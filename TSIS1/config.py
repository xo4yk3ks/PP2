# config.py

def load_config():
    return {
        "host":     "localhost",
        "database": "phonebook_db",
        "user":     "postgres",
        "password": "your_password",   # ← change this
        "port":     "5432"
    }

# Alias so older imports (from Practice 7) still work:
# from config import DB_CONFIG
DB_CONFIG = load_config()
