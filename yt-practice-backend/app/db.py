import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
# SNIPPETS import-dotenv-load_dotenv-reads-key-value-pairs
""" 
from dotenv import load_dotenv imports a helper that reads key-value pairs from a .env file and loads them into your environment variables 
at runtime, and load_dotenv() executes that process so your application can 
access values like DATABASE_URL via os.getenv() instead of hardcoding secrets or configuration directly in your code. 
"""

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg.connect(DATABASE_URL)