

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





# import discord
# from discord.ext import commands
# import os
# from googleapiclient.discovery import build
# from google_images_download import google_images_download
# import random
# from dotenv import load_dotenv
# load_dotenv() # this loads the .env file with our credentials
# #api_key - api key (google custom search api)
# #search_id - Programmable Search Engine id
# #token_id - discord bot token
# client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
# @client.event
# async def on_ready():
# 	print("Bot Is Online\n")
# @client.command(aliases=["show"])
# async def showpic(ctx,*,search):
# 	ran = random.randint(0, 9)
# 	resourse = build("customsearch", "v1", developerKey=(os.getenv('api_key'))).cse()
# 	result = resourse.list(q=f"{search}", cx=(os.getenv('search_id')), searchType="image").execute()
# 	url = result["items"][ran]["link"]
# 	embed1 = discord.Embed(title=f"Here Your Image ({search}) ")
# 	embed1.set_image(url=url)
# 	await ctx.send(embed=embed1)
# client.run(os.getenv('token_id'))