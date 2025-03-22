import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from fastapi import HTTPException
import uuid

load_dotenv()

class S3Client:
    def __init__(self):
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.getenv('AWS_REGION', 'eu-west-1')
        self.bucket_name = os.getenv('AWS_S3_BUCKET')
        
        if not all([self.aws_access_key_id, self.aws_secret_access_key, self.bucket_name]):
            raise ValueError("AWS credentials or bucket name not found in environment variables")
        
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    async def upload_file(self, file, folder: str = "images") -> str:
        """
        Upload a file to S3 bucket
        Returns the URL of the uploaded file
        """
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{folder}/{str(uuid.uuid4())}{file_extension}"
            
            # Upload file
            self.s3.upload_fileobj(
                file.file,
                self.bucket_name,
                unique_filename,
                ExtraArgs={
                    "ContentType": file.content_type,
                    "ACL": "public-read"
                }
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{unique_filename}"
            return url
            
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_file(self, file_url: str):
        """
        Delete a file from S3 bucket using its URL
        """
        try:
            # Extract key from URL
            key = file_url.split(f"{self.bucket_name}.s3.{self.region_name}.amazonaws.com/")[1]
            
            # Delete file
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

s3_client = S3Client() 