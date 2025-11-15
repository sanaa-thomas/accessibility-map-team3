from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector  # type: ignore
import os
from database import get_db_pool

router = APIRouter()
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "secret1234"),
    "database": os.getenv("DB_NAME", "campus_map"),
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Row-by-row search: iterate all accounts and compare
        cursor.execute("SELECT * FROM Admin")
        for row in cursor:
            # use 'password'
            if row.get("username") == request.username and row.get("password") == request.password:
                return {"success": True, "message": "Login successful"}
        # no match found
        raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Server error")
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn and conn.is_connected():
                conn.close()
        except Exception:
            pass
