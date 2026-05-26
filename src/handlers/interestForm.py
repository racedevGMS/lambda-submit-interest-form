import json
from db import save_submission
# from email_service import send_interest_form_email

def InterestFormSubmissionHandler(body):
    try:
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
