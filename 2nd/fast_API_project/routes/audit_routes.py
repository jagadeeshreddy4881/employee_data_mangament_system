from fastapi import APIRouter

audit_router = APIRouter()

# ==========================================
# AUDIT LOGS
# ==========================================
@audit_router.get("/audit-logs")
def audit_logs():

    return {
        "message": "Audit Logs API Working"
    }
