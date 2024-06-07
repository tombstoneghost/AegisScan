"""
Configuration File
"""
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(".")/".env"
load_dotenv(env_path)

class Config:
    """
    Class containing configuration variables
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    ZAP_API_KEY = os.getenv('ZAP_API_KEY')
    ZAP_API_URL = os.getenv('ZAP_API_URL')
