import json
import boto3
import csv
from io import StringIO
from io import BytesIO

import urllib.request

def entrypoint(event, context):

    filename = event.get('Records')[0].get('s3').get('object').get('key')
    bucketname = event.get('Records')[0].get('s3').get('bucket').get('name')
    output_bucketname = 'lambda1-output-files'
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3') 

    bucket = s3.Bucket(bucketname) 
    
    obj = s3_client.get_object(Bucket= bucketname, Key= filename)

    body = obj['Body'].read().decode('utf-8')
    lines = body.split('\n')
    
    reader = csv.DictReader(lines)
    
    for row in reader:
        keys = list(row.keys())
        values = list(row.values())
        print(keys[11], values[11])
        print(keys[15], values[15])
        url = values[15]
        
        file_name = url.split('/')[-1]
        response = urllib.request.urlopen(url)
        data = response.read()

        print(s3.Object(output_bucketname, file_name).put(Body=BytesIO(data)))
            
            
            
    body = {
        "message": "Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
  
