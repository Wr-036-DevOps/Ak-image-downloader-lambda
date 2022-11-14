

from bing_image_downloader import downloader
import os
import boto3
import io
from datetime import datetime
import uuid



def lambda_handler(event, context):
    animal_name = event["Records"][0]["body"]
    downloader.download(f"{animal_name}", limit=1, output_dir='/tmp/dataset/', adult_filter_off=True, force_replace=False, timeout=60)
    bucket_name = "BUCKET-NAME"
    file_name = f"/tmp/dataset/{animal_name}/Image_1.jpg"
    
    print(os.listdir(path=f"/tmp/dataset/{animal_name}"))
    
    #now = datetime.now().time() 
    #now = str(now)
    id = str(uuid.uuid4())
    key = id + ".jpg"
    with open(file_name, "rb") as f:
        image = f.read()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name=f'{bucket_name}')
    bucket.upload_fileobj(io.BytesIO(image), f"{key}")
    
    
    return {
        'statusCode': 200,
        'body': f"Upload succeeded: {file_name} has been uploaded to Amazon S3 in bucket {bucket_name}"
    }