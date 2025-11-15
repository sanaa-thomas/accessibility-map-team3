from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import mysql.connector  # type: ignore
import os

router = APIRouter()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "secret1234"),
    "database": os.getenv("DB_NAME", "campus_map"),
}

# ✅ Request model for threshold updates
class ThresholdUpdate(BaseModel):
    node_id: int

@router.put("/update_threshold")
def update_threshold(request: ThresholdUpdate):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT threshold FROM Nodes WHERE node_id=%s", (request.node_id,))
        node = cursor.fetchone()

        if not node:
            raise HTTPException(status_code=404, detail="Node does not exist")

        new_threshold = node["threshold"] + 1

        if new_threshold > 3:
            cursor.execute(
                "UPDATE Nodes SET threshold=%s, on_off=0 WHERE node_id=%s",
                (new_threshold, request.node_id)
            )
        else:
            cursor.execute(
                "UPDATE Nodes SET threshold=%s, on_off=1 WHERE node_id=%s",
                (new_threshold, request.node_id)
            )

        conn.commit()

        return {
            "success": True,
            "node_id": request.node_id,
            "new_threshold": new_threshold,
            "on_off_status": 0 if new_threshold > 3 else 1
        }

    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Server error")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ✅ Request model for submitting reports
class ReportRequest(BaseModel):
    report: str

@router.post("/report")
def submit_report(request: ReportRequest):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Reports (report_text) VALUES (%s)", (request.report,))
        conn.commit()

        return {"success": True, "message": "Report submitted"}

    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Server error")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
