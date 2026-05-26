import json
import traceback
from handlers.interestForm import *

ALLOWED_ORIGINS = [
    "https://dmjrwh9kv9rt1.cloudfront.net",
    "http://localhost:5173",
]

def _cors_headers(event):
    origin = (event.get("headers") or {}).get("origin", "")
    allowed = origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]
    return {
        "Access-Control-Allow-Origin": allowed,
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
    }

def handler(event, context):
    print("event:", event)

    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {"statusCode": 200, "headers": _cors_headers(event), "body": ""}

    try:
        raw = event.get("body", event)
        body = json.loads(raw) if isinstance(raw, str) else raw
        print("body:", body)

        if body["type"] == "submit interest form":
            result = InterestFormSubmissionHandler(body)
        else:
            result = {
                "statusCode": 500,
                "body": json.dumps({"message": f"Unknown type: {body.get('type')}"}),
            }
    except Exception as e:
        traceback.print_exc()
        result = {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
        }

    result["headers"] = _cors_headers(event)
    return result
