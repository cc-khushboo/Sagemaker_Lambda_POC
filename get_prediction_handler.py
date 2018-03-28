import json

import time
import os
from pydub import AudioSegment
from multiprocessing import Pool
import boto3
from io import BytesIO

def entrypoint(event, context):

	filename = event.get('Records')[0].get('s3').get('object').get('key')
    bucketname = event.get('Records')[0].get('s3').get('bucket').get('name')
    output_bucketname = 'wav_bucket'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname) 
	
	obj = s3.object(bucketname, filename)
	fileobj = BytesIO()
	obj.download_fileobj(fileobj)

	

	body = {
        "message": "Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response