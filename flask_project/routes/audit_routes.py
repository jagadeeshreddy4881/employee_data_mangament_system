from flask import (
    Blueprint,
    jsonify
)

from database.mongo import (
    audit_collection
)

# Blueprint for audit APIs
audit_bp = Blueprint(
    "audit_bp",
    __name__
)

# ==========================================
# AUDIT LOGS API
#
# Purpose:
# Returns all employee activity logs
# sorted by latest activity first.
# ==========================================

@audit_bp.route("/audit-logs")
def audit_logs():
    logs = list(
        audit_collection.find({},{"_id": 0}).sort("timestamp",-1)
    )
    return jsonify(logs)


