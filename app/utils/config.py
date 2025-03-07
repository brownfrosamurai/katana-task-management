import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
  AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
  AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
  AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
  DEBUG = os.getenv("DEBUG", "True") == "True"