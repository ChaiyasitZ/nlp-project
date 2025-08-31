import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Atlas Configuration
    # Default to Atlas connection, fallback to local if not provided
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/newstimelineai')
    
    # MongoDB Atlas specific settings
    MONGO_OPTIONS = {
        'retryWrites': True,
        'w': 'majority',
        'maxPoolSize': 50,
        'minPoolSize': 5,
        'maxIdleTimeMS': 30000,
        'serverSelectionTimeoutMS': 5000,
        'socketTimeoutMS': 20000,
        'connectTimeoutMS': 10000
    }
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # NLP Configuration
    MAX_ARTICLES_PER_REQUEST = int(os.environ.get('MAX_ARTICLES_PER_REQUEST', '20'))
    DEFAULT_LANGUAGE = os.environ.get('DEFAULT_LANGUAGE', 'th')  # Thai as default
    
    # Analysis Configuration
    SIMILARITY_THRESHOLD = float(os.environ.get('SIMILARITY_THRESHOLD', '0.3'))
    MAX_KEYWORDS = int(os.environ.get('MAX_KEYWORDS', '10'))
    MAX_ENTITIES = int(os.environ.get('MAX_ENTITIES', '15'))
    
    # Web Scraping Configuration
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '30'))
    USER_AGENT = os.environ.get('USER_AGENT', 'NewsTimelineAI/1.0')
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
