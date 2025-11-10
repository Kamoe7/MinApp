
import psycopg
from psycopg.rows import dict_row
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()
    
    
def get_connection():
    try:
        print('Connecting to DB')
        
        dsn = (
            Config.DATABASE_URL
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


