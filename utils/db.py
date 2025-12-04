import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    conn=duckdb.connect(os.getenv("DB_PATH"))
    return conn