from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import aiomysql # type: ignore
from database import get_db_pool

router = APIRouter()

# ✅ Request model for threshold updates
class ThresholdUpdate(BaseModel):
    node_id: int

@router.put("/update_threshold")
async def update_threshold(request: ThresholdUpdate):
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT threshold FROM Nodes WHERE node_id=%s", (request.node_id,))
                node = await cur.fetchone()

                if not node:
                    raise HTTPException(status_code=404, detail="Node does not exist")

                new_threshold = node["threshold"] + 1

                on_off = 0 if new_threshold > 3 else 1
                await cur.execute(
                    "UPDATE Nodes SET threshold=%s, on_off=%s WHERE node_id=%s",
                    (new_threshold, on_off, request.node_id)
                )
                await conn.commit()

                return {
                    "success": True,
                    "node_id": request.node_id,
                    "new_threshold": new_threshold,
                    "on_off_status": on_off
                }

    except Exception as e:
        print("DB Error:", e, flush=True)
        raise HTTPException(status_code=500, detail="Server error")


class ReportRequest(BaseModel):
    report: str


@router.post("/report")
async def submit_report(request: ReportRequest):
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO Reports (report_text) VALUES (%s)", (request.report,))
                await conn.commit()

        return {"success": True, "message": "Report submitted"}

    except Exception as e:
        print("DB Error:", e, flush=True)
        raise HTTPException(status_code=500, detail="Server error")
