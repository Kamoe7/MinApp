import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # DB_HOST = os.getenv('DB_HOST', 'localhost')
    # DB_NAME = os.getenv('DB_NAME', 'translations_db')
    # DB_USER = os.getenv('DB_USER', 'postgres')
    # DB_PASSWORD = os.getenv('DB_PASSWORD')
    # DB_PORT = os.getenv('DB_PORT')
    
    DATABASE_URL = os.getenv('DATABASE_URL')

    # JWT
    SECRET_KEY = os.getenv(
        'SECRET_KEY')

    # Cache
    CACHE_DURATION = 300  # 5 minutes

    # CORS
    CORS_ORIGINS = ['http://localhost:5173',
                    'http://localhost:3000', 'https://minapp-81ss.onrender.com']
