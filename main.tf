terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 4.16"
            
        }
    }
}

provider "aws" {
    region  = "eu-central-1"
    default_tags {
                tags = {
                Key = "ita_group"
                Value = "Wr-36"
                }   
            } 
    # access_key = "my-access-key"
    # secret_key = "my-secret-key"
}

#Creating Lambda Role
resource "aws_iam_role" "Training-lambda_image_downloader_role" {
    name = "Training-lambda_image_downloader_role"
    permissions_boundary  = "arn:aws:iam::536460581283:policy/boundaries/CustomPowerUserBound"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Sid    = ""
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            },
        ]
    })
}


#Attaching S3 access policy
resource "aws_iam_role_policy_attachment" "S3-access-policy" {
    role       = "${aws_iam_role.Training-lambda_image_downloader_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}



#Creating Public S3 Bucket
resource "aws_s3_bucket" "b" {
    bucket_prefix = "lambda-images"
}
resource "aws_s3_bucket_public_access_block" "example" {
    bucket = "${aws_s3_bucket.b.id}"
    block_public_policy = false
    
}

#Attaching S3 Policy

resource "aws_s3_bucket_policy" "Public_access" {
    bucket = aws_s3_bucket.b.id
    #policy = data.aws_iam_policy_document.allow_access_from_another_account.json
    policy = <<EOF
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Principal": "*",
			"Action": "s3:GetObject",
			"Resource": "${aws_s3_bucket.b.arn}/*"
        
		}
	]
}
EOF
}




#Creating Lambda Fxn 

resource "aws_lambda_function" "test_lambda" {
    filename      = "my-deployment-package.zip"
    function_name = "image-downloader"
    role          = aws_iam_role.Training-lambda_image_downloader_role.arn
    runtime       = "python3.8"
    handler       = "lambda_handler"
}