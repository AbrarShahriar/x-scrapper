import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Server configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Twitter API limits
    MAX_TWEETS_PER_USER = 50
    MAX_USERS_PER_REQUEST = 5
    MAX_TWEETS_MULTIPLE_USERS = 20
    
    # Cache settings
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'False').lower() == 'false'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 1800))  # 30 minutes
    CACHE_MAXSIZE = int(os.getenv('CACHE_MAXSIZE', 500))