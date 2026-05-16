import os
import uuid
from datetime import datetime, timezone
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "interest_form_submissions"
_REGION    = os.getenv("AWS_REGION", "us-east-1")
_ENDPOINT  = os.getenv("DYNAMODB_ENDPOINT_URL")

def _table():
    kwargs = {"region_name": _REGION}
    if _ENDPOINT:
        kwargs["endpoint_url"] = _ENDPOINT
    return boto3.resource("dynamodb", **kwargs).Table(TABLE_NAME)

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def save_submission(full_name: str, email: str, phone: str, interest: str, message: str) -> dict[str, Any]:
    item = {
        "submission_id": str(uuid.uuid4()),
        "created_at":    _now_iso(),
        "full_name":     full_name,
        "email":         email,
        "phone":         phone,
        "interest":      interest,
        "message":       message,
    }
    _table().put_item(Item=item)
    return item

def get_submission(submission_id: str, created_at: str) -> dict[str, Any] | None:
    response = _table().get_item(Key={"submission_id": submission_id, "created_at": created_at})
    return response.get("Item")

def list_by_email(email: str) -> list[dict[str, Any]]:
    response = _table().query(
        IndexName="email-created_at-index",
        KeyConditionExpression=Key("email").eq(email),
        ScanIndexForward=False,
    )
    return response.get("Items", [])

def list_recent(limit: int = 50) -> list[dict[str, Any]]:
    items = _table().scan(Limit=limit).get("Items", [])
    return sorted(items, key=lambda x: x["created_at"], reverse=True)
