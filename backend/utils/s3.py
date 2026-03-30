import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),  # <-- IMPORTANT for LocalStack
        config=Config(signature_version="s3v4"),
    )

def create_presigned_upload_url(object_name, expiration=3600):
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_post(
            Bucket=S3_BUCKET_NAME,
            Key=object_name,
            Fields={"Content-Type": "application/pdf"},
            Conditions=[
                {"Content-Type": "application/pdf"},
                ["content-length-range", 0, 10485760]
            ],
            ExpiresIn=3600
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None
    
def upload_file_to_s3(file, object_key):
    s3 = get_s3_client()
    bucket = os.getenv("S3_BUCKET_NAME")

    s3.upload_fileobj(file.file, bucket, object_key)


# def create_presigned_download_url(object_name, expiration=3600):
#     s3_client = get_s3_client()
#     try:
#         response = s3_client.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': S3_BUCKET_NAME, 'Key': object_name},
#             ExpiresIn=expiration
#         )
#         return response
#     except ClientError as e:
#         print(f"Error generating presigned URL: {e}")
#         return None


def create_presigned_download_url(object_key: str):
    try:
        s3 = get_s3_client()  # <-- FIX: call the function

        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET_NAME, "Key": object_key},
            ExpiresIn=3600,
        )

        # Fix LocalStack hostname for browser
        url = url.replace("localstack", "localhost")

        return url

    except Exception as e:
        print("Error generating presigned URL:", e)
        return None

