import json
from handlers.interestForm import *

def handler(event, context):
    print('event: ', event)
    body = json.loads(event['body'])
    print('body: ', body)
    if body['type'] == 'interest form submission':
        return InterestFormSubmissionHandler(body)

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