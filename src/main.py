import json
from handlers.interestForm import *

def handler(event, context):
    body = json.loads(event['body'])

    if body['type'] == 'interest form submission':
        InterestFormSubmissionHandler(body)

def InterestFormSubmissionHandler(body):
    form = body['data']
    print("Form data received:")
    print(form)
    # Process the interest form submission
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Interest form submitted successfully'})
    }