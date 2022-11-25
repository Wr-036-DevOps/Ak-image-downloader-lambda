

from bing_image_downloader import downloader
import os
import boto3
import uuid
import json
from pathlib import Path




def lambda_handler(event, context):
    # Extracting parameter from the SQS json mesage #Python dictionary
    data = json.loads(event['Records'][0]["body"])
    animal = data["animal"]
    number = int(data['number'])
    print(f"we are downloading {number} pictures of {animal}")


    # Downloading the number of pictures of given animal
    downloader.download(f"{animal}", limit=number, output_dir='/tmp/dataset/', adult_filter_off=True, force_replace=False, timeout=60)
    
    
    bucket_name = os.environ['bucket_name']
    path = f"/tmp/dataset/{animal}/"
    client = boto3.client("s3")


    # Uploading downloaded images to s3
    for image in os.listdir(path):
        id = str(uuid.uuid4())
        key = id + ".jpg"

    # Creating file name ie with full path for open()
        file = str(path) + str(image)
        with open(file, "rb") as f:
            client.put_object(
                Bucket=bucket_name,
                Body=f,
                Key=key
        )
    return {
        'statusCode': 200,
        'body': f"Upload succeeded: Upload to Amazon S3 bucket {bucket_name} complete"
    }