import json
from main import main

def lambda_handler(event, context):
    
    main()
    return {
        'statusCode': 200,
        'body': []
    }
