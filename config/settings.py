from functools import lru_cache
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL:str = os.environ['MONGODB_URL']
    # USERNAME:str = os.environ['USERNAME']
    # PASSWORD:str = os.environ['PASSWORD']
    APP_SECRET_KEY:str = os.environ['APP_SECRET_KEY']
    ALLOWED_HOSTS:list = ['*']
    GOOGLE_CLIENT_ID:str= os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET:str=os.environ['GOOGLE_CLIENT_SECRET']
    GOOGLE_REDIRECT_URI:str = os.environ['GOOGLE_REDIRECT_URI']
    #  = os.environ['']

@lru_cache
def get_settings():
    return Settings()