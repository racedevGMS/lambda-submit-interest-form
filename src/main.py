import json
from handlers.interestForm import *

def handler(event, context):
    try:
        print('event: ', event)
        raw = event.get('body', event)
        body = json.loads(raw) if isinstance(raw, str) else raw
        print('body: ', body)
        if body['type'] == 'submit interest form':
            return InterestFormSubmissionHandler(body)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Unknown type: {body.get('type')}"})
        }
    except Exception as e:
        print(f"Error in handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }

def InterestFormSubmissionHandler(body):
    try:
        form = body['data']
        print("Form data received:")
        print(form)
        # Process the interest form submission

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Interest form submitted successfully'})
        }
    except Exception as e:
        print(f"Error processing interest form: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to process interest form submission'})
        }