import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "brains")
MAIN_DB = os.path.join(BASE_DIR, "brains/brain.db")
DAY = 86400  # POSIX day (exact value)
MINUTE = 60

