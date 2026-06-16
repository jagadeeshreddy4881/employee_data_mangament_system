# MongoDB client library
from pymongo import MongoClient

# Loads variables from .env file
from dotenv import load_dotenv

# Used to read environment variables
import os

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================
# Reads .env file
load_dotenv()

# ==========================================
# MONGODB CONNECTION
# ==========================================
# Reads MongoDB Connection string from .env
client = MongoClient(os.getenv("MONGO_URI"))

#check whether mongodb is reachable
try:
     # Ping database server to check connection
    client.admin.command("ping")
    print("MongoDB Ping Successful")
except Exception as e:
    print("MongoDB Ping Failed")
    print(e)

# Select database    
db = client[os.getenv("DB_NAME")]

# Select collection
collection = db[os.getenv("COLLECTION_NAME")]
print("MongoDB Connected Successfully")

# ==========================================
# AUDIT LOG COLLECTION
#
# Stores all employee activity logs
# ==========================================

audit_collection = db["audit_logs"]
# MongoDB client library
from pymongo import MongoClient

# Loads variables from .env file
from dotenv import load_dotenv

# Used to read environment variables
import os

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================
# Reads .env file
load_dotenv()

# ==========================================
# MONGODB CONNECTION
# ==========================================
# Reads MongoDB Connection string from .env
client = MongoClient(os.getenv("MONGO_URI"))

#check whether mongodb is reachable
try:
     # Ping database server to check connection
    client.admin.command("ping")
    print("MongoDB Ping Successful")
except Exception as e:
    print("MongoDB Ping Failed")
    print(e)

# Select database    
db = client[os.getenv("DB_NAME")]

# Select collection
collection = db[os.getenv("COLLECTION_NAME")]
print("MongoDB Connected Successfully")

# ==========================================
# AUDIT LOG COLLECTION
#
# Stores all employee activity logs
# ==========================================

audit_collection = db["audit_logs"]
# MongoDB client library
from pymongo import MongoClient

# Loads variables from .env file
from dotenv import load_dotenv

# Used to read environment variables
import os

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================
# Reads .env file
load_dotenv()

# ==========================================
# MONGODB CONNECTION
# ==========================================
# Reads MongoDB Connection string from .env
client = MongoClient(os.getenv("MONGO_URI"))

#check whether mongodb is reachable
try:
     # Ping database server to check connection
    client.admin.command("ping")
    print("MongoDB Ping Successful")
except Exception as e:
    print("MongoDB Ping Failed")
    print(e)

# Select database    
db = client[os.getenv("DB_NAME")]

# Select collection
collection = db[os.getenv("COLLECTION_NAME")]
print("MongoDB Connected Successfully")

# ==========================================
# AUDIT LOG COLLECTION
#
# Stores all employee activity logs
# ==========================================

audit_collection = db["audit_logs"]
print("MongoDB Connected Successfully")