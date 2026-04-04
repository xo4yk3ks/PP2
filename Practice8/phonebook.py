
# phonebook.py

import psycopg2
from config import load_config

def run():
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:

            # Example: call function
            cur.execute("SELECT * FROM search_phonebook(%s)", ('John',))
            print(cur.fetchall())

            # Example: call procedure
            cur.execute("CALL upsert_user(%s, %s)", ('John', '+1234567890'))

if __name__ == '__main__':
    run()
