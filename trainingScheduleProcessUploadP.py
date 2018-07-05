from __future__ import print_function

import json
import urllib
import boto3

print('Loading function')

s3 = boto3.resource('s3')

# Triggered by:  Object Create in 'training-schedule' bucket.
# Take incoming file, rename it to training-schedule/ready/current-schedule.csv.
def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Determine the bucket / key of the newly uploaded object:
    bucketName = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    print('Moving {}/{} to {}/ready/current-schedule.csv...'.format(bucketName, key, bucketName))
    
    # Copy:
    try:
        copy_source = {
            'Bucket': bucketName,
            'Key': key
        }
        bucket = s3.Bucket(bucketName)
        obj = bucket.Object('ready/current-schedule.csv')
        obj.copy(copy_source)
    except Exception as e:
        print(e)
        print('Error copying {}/{} to {}/ready/current-schedule.csv.'.format(bucketName, key, bucketName))
        raise e
        
    # Remove original:    
    try:
        delete_params = {
            'Bucket': bucketName,
            'Key': key
        }
        s3.Object(bucketName,key).delete()
            
    except Exception as e:
        print(e)
        print('Error deleting {}/{}.'.format(bucketName, key))
        raise e

    print('Object successfully moved.')