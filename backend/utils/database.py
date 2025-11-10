
import psycopg
from psycopg.rows import dict_row
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()
    
    
def get_connection():
    try:
        print('Connecting to DB')
        print(f"Host:{Config.DB_HOST}")
        print(f"DB:{Config.DB_NAME}")
        print(f"User:{Config.DB_USER}")
        
        dsn = (
            f"postgresql://"
            f"{Config.DB_USER}:{Config.DB_PASSWORD or ''}"
            f"@{Config.DB_HOST}:{Config.DB_PORT or 5432}"
            f"/{Config.DB_NAME}"
        )
        conn = psycopg.connect(
            dsn,
            row_factory=dict_row
        )
        print("Connection Successful!")

        return conn
    
    except psycopg.OperationalError as e:
        print(f"DB connction failed")
        print(f"Error:{e}")
    except Exception as e:
        print(f"Error:{type(e).__name__}:{e}")
        raise


