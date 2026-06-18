# ==========================================
# FASTAPI IMPORTS
# ==========================================

from fastapi import APIRouter

# ==========================================
# CREATE ROUTER
# ==========================================

system_router = APIRouter()

# ==========================================
# DATABASE TEST API
# ==========================================

from fastapi import APIRouter
from database.mongo import collection

system_router = APIRouter()

# ==========================================
# DATABASE TEST API
# ==========================================

@system_router.get("/dbtest")
def db_test():

    try:
        # Try fetching one document
        collection.find_one()

        return {
            "status": "Success",
            "message": "Database Connected Successfully"
        }

    except Exception as e:

        return {
            "status": "Failed",
            "message": "Database Connection Failed",
            "error": str(e)
        }

# ==========================================
# HELLO API
# ==========================================

@system_router.get("/hello")
def hello():

    return {
        "message": "Hello User ,' Ready to useFastAPI!'"
    }