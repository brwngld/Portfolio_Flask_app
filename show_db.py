import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")

# Connect to MySQL
conn = pymysql.connect(
    host=str(MYSQL_HOST), user=str(MYSQL_USER), password=str(MYSQL_PASSWORD)
)

cur = conn.cursor()

# Execute SQL query to retrieve all databases
cur.execute("SHOW DATABASES")

# Fetch all rows from the result set
databases = cur.fetchall()

# Print the list of databases
print("List of databases:")
for db in databases:
    print(db[0])

conn.close()
