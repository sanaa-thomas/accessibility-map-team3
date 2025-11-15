# test_db.py
import os
import pymysql    # type: ignore # sync test; pymysql is a dependency of aiomysql
host = os.getenv("DB_HOST", "127.0.0.1")
user = os.getenv("DB_USER", "root")
pw   = os.getenv("DB_PASSWORD", "")
db   = os.getenv("DB_NAME", "campus_map")
port = int(os.getenv("DB_PORT", "3306"))

print("Trying", user, "@", host, "port", port)
try:
    conn = pymysql.connect(host=host, user=user, password=pw, db=db, port=port)
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("OK:", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("ERROR:", type(e).__name__, e)