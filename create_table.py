import os

import pymysql
from dotenv import load_dotenv

# Load the .env file in the current folder
load_dotenv()

# Read values
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# Debug check
if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB]):
    raise ValueError(
        "One or more required environment variables are missing. Check your .env file."
    )

# Connect to MySQL
conn = pymysql.connect(
    host=str(MYSQL_HOST), user=str(MYSQL_USER), password=str(MYSQL_PASSWORD)
)


cur = conn.cursor()
cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
conn.close()

print(f"Database '{MYSQL_DB}' created successfully!")
