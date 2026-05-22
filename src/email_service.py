import os
import boto3

_REGION     = os.getenv("AWS_REGION", "us-east-1")
_FROM_EMAIL = os.getenv("NOTIFY_FROM_EMAIL")
_TO_EMAIL   = os.getenv("NOTIFY_TO_EMAIL")

def send_interest_form_email(form: dict, submission_id: str) -> None:
    subject = f"New Interest Form Submission – {form['full_name']}"
    body = (
        f"A new interest form was submitted.\n\n"
        f"Name:      {form['full_name']}\n"
        f"Email:     {form['email']}\n"
        f"Phone:     {form['phone']}\n"
        f"Interest:  {form['interest']}\n"
        f"Message:   {form.get('message', '')}\n\n"
        f"Submission ID: {submission_id}"
    )
    boto3.client("ses", region_name=_REGION).send_email(
        Source=_FROM_EMAIL,
        Destination={"ToAddresses": [_TO_EMAIL]},
        Message={
            "Subject": {"Data": subject},
            "Body":    {"Text": {"Data": body}},
        },
    )
