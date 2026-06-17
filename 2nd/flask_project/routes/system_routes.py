from flask import Blueprint

from database.mongo import collection

# Blueprint for system APIs
system_bp = Blueprint(
    "system_bp",
    __name__
)



# ==========================================
# DATABASE TEST API
# URL:
# http://localhost:5000/dbtest
#
# Purpose:
# Verify MongoDB connection
# ==========================================

#dbtest route to check MongoDB connection
@system_bp.route("/dbtest")
def dbtest():
    try:
        
        # Count documents in collection
        # If this works, MongoDB is connected
        collection.count_documents({})
        return "MongoDB Connected"
    except Exception as e:
        return str(e)
    

#check connection
@system_bp.route("/hello")
def hello():
    return "Hello user"


