
# connect.py

import psycopg2
from config import load_config

def get_connection():
    config = load_config()
    return psycopg2.connect(**config)
