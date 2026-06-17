#Used to store: date and time for every action
from datetime import datetime

from database.mongo import audit_collection


# ==========================================
# AUDIT LOGGER
#
# Purpose:
# Store employee activity logs.
#
# Why:
# Track all important operations.
# ==========================================

def create_audit_log(
    action,
    employee_id,
    message
):

    audit_collection.insert_one({

        "action": action,

        "employee_id": employee_id,

        "message": message,

        "timestamp":
            datetime.now()
    })

