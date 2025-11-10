
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
import os
    
    
def get_connection():
    try:
        print('Connecting to DB')
        print(f"Host:{Config.DB_HOST}")
        print(f"DB:{Config.DB_NAME}")
        print(f"User:{Config.DB_USER}")
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
            cursor_factory=RealDictCursor
        )
        print("Connection Successful!")

        return conn
    except psycopg2.OperationalError as e:
        print(f"DB connction failed")
        print(f"Error:{e}")
    except Exception as e:
        print(f"Error:{type(e).__name__}:{e}")
        raise


