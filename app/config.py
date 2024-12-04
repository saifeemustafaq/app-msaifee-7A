import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = "irchkrlnRApovknwqZUxRZbYj9IKZlt/34HTDwtjBsjXRAeSgqndMELSstBcoEoe0uTVGqseEm0Ya2LTCQy5Zw=="
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False