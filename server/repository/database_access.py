import os

from contextlib import contextmanager
from mysql.connector import connect
from load_dotenv import load_dotenv

load_dotenv('.env')

@contextmanager
def get_db_connection():
    conn = connect(
        host = os.environ['DB_HOST'],
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        database = os.environ['DB_NAME']
    )
    try:
        cursor = conn.cursor(dictionary=True)
        yield conn, cursor
    finally:
        conn.close()
        cursor.close()
