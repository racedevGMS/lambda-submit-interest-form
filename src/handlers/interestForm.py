import json
import os
import urllib.request
import urllib.parse
from db import save_submission
from email_service import send_interest_form_email

_RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET_KEY")
_RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"
_SCORE_THRESHOLD = 0.5

def _verify_recaptcha(token: str) -> bool:
    data = urllib.parse.urlencode({
        "secret": _RECAPTCHA_SECRET,
        "response": token,
    }).encode()
    req = urllib.request.Request(_RECAPTCHA_URL, data=data)
    with urllib.request.urlopen(req, timeout=5) as resp:
        result = json.loads(resp.read())
    return result.get("success") and result.get("score", 0) >= _SCORE_THRESHOLD

def InterestFormSubmissionHandler(body):
    try:
        token = body.get("recaptchaToken")
        if not token or not _verify_recaptcha(token):
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "reCAPTCHA verification failed"}),
            }

        form = body['data']
        item = save_submission(
            full_name=form['full_name'],
            email=form['email'],
            phone=form['phone'],
            interest=form['interest'],
            message=form.get('message', ''),
        )
        print("Saved submission:", item['submission_id'])
        # send_interest_form_email(form, item['submission_id'])
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Interest form submitted successfully', 'id': item['submission_id']})
        }
    except KeyError as e:
        print(f"Missing field: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f"Missing required field: {e}"})
        }
    except Exception as e:
        print(f"Error processing interest form: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to process interest form submission'})
        }