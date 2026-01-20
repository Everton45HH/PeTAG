import psycopg2
import psycopg2.extras
import os
import dotenv

dotenv.load_dotenv()

class Database:
    def get_connection(self):
        DATABASE_URL = os.environ.get("DATABASE_URL")
        
        conn = psycopg2.connect(DATABASE_URL)
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        return conn, cursor