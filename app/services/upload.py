import boto3
from app.utils.config import Config

# Initialize AWS S3 Client
class UploadService:
  s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
  )

  @staticmethod
  def to_s3(image_buffer, filename):
    """Uploads an image to AWS S3 and returns the file URL."""
    bucket_name = Config.AWS_S3_BUCKET
    UploadService.s3_client.upload_fileobj(image_buffer, bucket_name, filename, ExtraArgs={'ContentType': 'image/png'})
    return f"https://{bucket_name}.s3.amazonaws.com/{filename}"