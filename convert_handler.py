import json
import boto3
import os


def entrypoint(event, context):

	print(event)
	key = event.get('Records')[0].get('s3').get('object').get('key')
	bucketname = event.get('Records')[0].get('s3').get('bucket').get('name')
	output_bucketname = 'wav-bucket'
	
	ets_client = boto3.client('elastictranscoder')

	response = ets_client.create_job(
		PipelineId='1521786113917-zecr0s',
		Input={
			'Key': key
		},
		Output={
			'Key': key[:-3] + 'wav',
			'PresetId': '1351620000001-300200',
	})
	print(response)


	

	response_body = {
        "message": "Your function executed successfully!",
		"input": event
    }

	response = {
		"statusCode": 200,
		"body": json.dumps(response_body)
	}

	return response

def old_version_entrypoint(event, context):
	print(event)
	key = event.get('Records')[0].get('s3').get('object').get('key')
	bucketname = event.get('Records')[0].get('s3').get('bucket').get('name')
	output_bucketname = 'wav-bucket'
	s3 = boto3.resource('s3')

	obj = s3.Object(bucketname, key)
	
	localInputFilePath = '/tmp/{}'.format(os.path.basename(key))
	localOutputFilePath = '/tmp/output/{}'.format(os.path.basename(key))

	print(localInputFilePath)
	obj.download_file(localInputFilePath)

	wavpath = localOutputFilePath[:-3] + 'wav'
	print(wavpath)


	#sound = AudioSegment.from_mp3(localInputFilePath)

	ff = FFmpeg(inputs={localInputFilePath: None},outputs={wavpath: None})
	ff.run()
	print(os.path.isfile(wavpath))

	

	response_body = {
        "message": "Your function executed successfully!",
		"input": event
    }

	response = {
		"statusCode": 200,
		"body": json.dumps(response_body)
	}

	return response