"""
create_table.py
---------------
Run once to provision the interest_form_submissions DynamoDB table.

Usage:
    python create_table.py                          # uses default AWS profile / env vars
    python create_table.py --region us-east-1       # explicit region
    python create_table.py --endpoint http://localhost:8000  # local DynamoDB

Requirements:
    pip install boto3
"""

import argparse
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "interest_form_submissions"


def create_table(region: str, endpoint_url: str | None = None) -> None:
    kwargs = {"region_name": region}
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url

    dynamodb = boto3.client("dynamodb", **kwargs)

    # Check if table already exists
    try:
        dynamodb.describe_table(TableName=TABLE_NAME)
        print(f"✅ Table '{TABLE_NAME}' already exists — skipping creation.")
        return
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceNotFoundException":
            raise

    print(f"Creating table '{TABLE_NAME}' ...")

    response = dynamodb.create_table(
        TableName=TABLE_NAME,

        # ----- Key schema -----
        # submission_id  : partition key (UUID v4 string)
        # created_at     : sort key (ISO-8601 UTC string, e.g. "2025-06-01T14:32:00Z")
        #                  lets you query all submissions sorted by time cheaply.
        AttributeDefinitions=[
            {"AttributeName": "submission_id", "AttributeType": "S"},
            {"AttributeName": "created_at",    "AttributeType": "S"},
            {"AttributeName": "email",         "AttributeType": "S"},  # ← add this
        ],
        KeySchema=[
            {"AttributeName": "submission_id", "KeyType": "HASH"},
            {"AttributeName": "created_at",    "KeyType": "RANGE"},
        ],

        # ----- GSI: look up all submissions by email -----
        GlobalSecondaryIndexes=[
            {
                "IndexName": "email-created_at-index",
                "KeySchema": [
                    {"AttributeName": "email",      "KeyType": "HASH"},
                    {"AttributeName": "created_at", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],

        # PAY_PER_REQUEST = on-demand (no capacity planning needed for a form)
        BillingMode="PAY_PER_REQUEST",

        # TTL attribute name — enable TTL in the console/CLI if you want
        # submissions auto-deleted after N days (set ttl_expiry epoch int on items).
        # Leaving the definition here as a reminder; it's harmless if unused.
        SSESpecification={"Enabled": True},  # encryption at rest
    )

    waiter = dynamodb.get_waiter("table_exists")
    waiter.wait(TableName=TABLE_NAME)

    print(f"✅ Table created successfully.")
    print(f"   ARN : {response['TableDescription']['TableArn']}")
    print(f"   GSI : email-created_at-index")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create DynamoDB interest form table")
    parser.add_argument("--region",   default="us-east-1", help="AWS region")
    parser.add_argument("--endpoint", default=None,        help="DynamoDB endpoint URL (local dev)")
    args = parser.parse_args()

    create_table(region=args.region, endpoint_url=args.endpoint)
