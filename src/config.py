import os
from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database configuration class"""
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT')

    def get_connection_params(self):
        """Return database connection parameters"""
        return {
            'host': self.host,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'port': self.port
        }

@contextmanager
def get_db_connection():
    """Database connection context manager"""
    conn = None
    try:
        db_config = DatabaseConfig()
        conn = psycopg2.connect(**db_config.get_connection_params())
        yield conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn is not None:
            conn.close()

@contextmanager
def get_db_cursor(conn):
    """Database cursor context manager"""
    cursor = None
    try:
        cursor = conn.cursor()
        yield cursor
    except psycopg2.Error as e:
        print(f"Cursor error: {e}")
        raise
    finally:
        if cursor is not None:
            cursor.close()

# Usage example:
# def main():
#     try:
#         with get_db_connection() as conn:
#             with get_db_cursor(conn) as cur:
#                 print("Database connection and cursor created successfully")
#                 # Your database operations here
#     except psycopg2.Error as e:
#         print(f"Database error: {e}")
#         return False
#     return True

# if __name__ == "__main__":
#     main()
