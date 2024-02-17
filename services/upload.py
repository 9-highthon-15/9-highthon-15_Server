import io
import boto3
from services.config import *

s3 = boto3.client(
    service_name="s3",
    endpoint_url=CF_ENDPOINT,
    aws_access_key_id=CF_ACCESS_KEY,
    aws_secret_access_key=CF_SECRET_KEY,
    region_name="auto",
)


def uploadImage(file, filename):
    file = io.BytesIO(file.read())
    try:
        s3.upload_fileobj(
            file,
            CF_BUCKET,
            filename,
        )
        return {
            "result": True,
            "code": "SUCCESS",
            "message": f"{CF_PUBLIC}/{filename}",
        }
    except Exception as e:
        return {
            "result": False,
            "code": "UPLOAD_ERROR",
            "message": str(e),
        }
