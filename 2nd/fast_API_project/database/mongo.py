# ==========================================
# MONGODB IMPORTS
# ==========================================

from pymongo import MongoClient
from dotenv import load_dotenv

import os

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# CONNECT TO MONGODB
# ==========================================

client = MongoClient(
    os.getenv("MONGO_URI")
)

# ==========================================
# CHECK DATABASE CONNECTION
# ==========================================

try:

    client.admin.command("ping")

    print("MongoDB Connected Successfully")

except Exception as e:

    print("MongoDB Connection Failed")

    print(e)

# ==========================================
# SELECT DATABASE
# ==========================================

db = client[
    os.getenv("DB_NAME")
]

# ==========================================
# SELECT EMPLOYEE COLLECTION
# ==========================================

collection = db[
    os.getenv("COLLECTION_NAME")
]

# ==========================================
# AUDIT COLLECTION
# ==========================================

audit_collection = db[
    "audit_logs"
]