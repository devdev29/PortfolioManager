import os

from contextlib import contextmanager
from psycopg2 import connect
from psycopg2.extras import RealDictCursor, register_uuid
from load_dotenv import load_dotenv

load_dotenv('.env')
register_uuid()

@contextmanager
def get_db_connection():
    conn = connect(
        host = os.environ['DB_HOST'],
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        dbname = os.environ['DB_NAME'],
        port = int(os.environ['DB_PORT'])
    )
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        yield conn, cursor
    finally:
        conn.close()
        cursor.close()
