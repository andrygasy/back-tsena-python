import boto3
from botocore.client import Config
from fastapi import UploadFile
import os

MINIO_URL = "http://51.38.237.164:9101"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"
BUCKET_NAME = "bucket"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
)

def upload_file(file: UploadFile, object_name: str = None) -> str:
    if object_name is None:
        object_name = file.filename
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, object_name)
        return f"{MINIO_URL}/{BUCKET_NAME}/{object_name}"
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def delete_file(object_name: str):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=object_name)
    except Exception as e:
        print(f"Error deleting file: {e}")

def get_file_url(object_name: str) -> str:
    return f"{MINIO_URL}/{BUCKET_NAME}/{object_name}"
