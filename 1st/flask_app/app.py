# Flask imports
# Flask -> creates web application
# request -> reads incoming HTTP requests
# jsonify -> returns JSON response
# render_template -> loads HTML pages
from flask import Flask, request, jsonify, render_template

# MongoDB client library
from pymongo import MongoClient

# Loads variables from .env file
from dotenv import load_dotenv

# Used to read environment variables
import os

# Used to read CSV files
import pandas as pd

#Used to store: date and time for every action
from datetime import datetime

# ==========================================
# FILE EXPORT LIBRARIES
# ==========================================

# send_file
# Used to return downloadable files
# from Flask APIs
from flask import send_file

# csv
# Built-in Python module used to
# create and write CSV files
import csv

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================
# Reads .env file
load_dotenv()


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================
app = Flask(__name__)


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

# ==========================================
# DATABASE TEST API
# URL:
# http://localhost:5000/dbtest
#
# Purpose:
# Verify MongoDB connection
# ==========================================

#dbtest
@app.route("/dbtest")
def dbtest():
    try:
        
        # Count documents in collection
        # If this works, MongoDB is connected
        collection.count_documents({})
        return "MongoDB Connected"
    except Exception as e:
        return str(e)
    

#check connection
@app.route("/hello")
def hello():
    return "Hello user"


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# POST API - Insert Single or Bulk Employees
@app.route("/employee", methods=["POST"])
def add_employee():

    data = request.get_json()

    # Bulk Insert
    if isinstance(data, list):

        inserted = 0

        for emp in data:

            existing = collection.find_one(
                {"id": emp["id"]}
            )

            if not existing:
                collection.insert_one(emp)
                inserted += 1

        return jsonify({
            "message": "Bulk insert completed",
            "inserted_count": inserted
        })



    # Single Insert
    existing = collection.find_one(
        {"id": data["id"]}
    )

    if existing:
        return jsonify({
            "message": "Employee already exists"
        }), 409

    result = collection.insert_one(data)
    create_audit_log(
    "ADD",
    data["id"],
    "Employee added"
    )
    
    return jsonify({
        "message": "Employee inserted successfully",
        "inserted_id": str(result.inserted_id)
    })



#remove_duplicates
@app.route("/remove-duplicates")
def remove_duplicates():

    seen = set()
    deleted = 0

    for doc in collection.find():

        emp_id = doc.get("id")

        if emp_id in seen:
            collection.delete_one(
                {"_id": doc["_id"]}
            )
            deleted += 1
        else:
            seen.add(emp_id)

    return jsonify({
        "message": "Duplicates removed",
        "deleted_count": deleted
    })


# ==========================================
# UPDATE EMPLOYEE
# ==========================================

@app.route("/employee/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):

    data = request.get_json()

    update_fields = {}

    # Only update fields provided by user

    if "present_salary" in data:
        update_fields["present_salary"] = int(
            data["present_salary"]
        )

    if "expected_hike" in data:
        update_fields["expected_hike"] = int(
            data["expected_hike"]
        )

    if "performance_rating" in data:
        update_fields["performance_rating"] = float(
            data["performance_rating"]
        )

    if "work_location" in data:
        update_fields["work_location"] = (
            data["work_location"]
        )

    if "role" in data:
        update_fields["role"] = (
            data["role"]
        )

    # Nothing entered

    if not update_fields:

        return jsonify({
            "message":
            "No fields provided for update"
        }), 400

    result = collection.update_one(
        {"id": emp_id},
        {"$set": update_fields}
    )

    if result.matched_count == 0:

        return jsonify({
            "message":
            "Employee not found"
        }), 404
    
    #create AUDIT log to track employee update activity.
    #to maintain history of changes made in records.
    
    create_audit_log(
        "UPDATE",
        emp_id,
        "Employee updated"
    )

    return jsonify({
        "message":
        "Employee updated successfully"
    })

@app.route("/test-update")
def test_update():

    result = collection.update_one(
        {"id": 1001},
        {
            "$set": {
                "present_salary": 200000
            }
        }
    )

    return jsonify({
        "matched": result.matched_count,
        "modified": result.modified_count
    })

# ==========================================
# FETCH EMPLOYEES API
#
# Purpose:
# Fetch employees using filters
#
# Supported Filters:
# id
# work_location
# salary_min
# salary_max
# expected_hike
# performance_rating
# role
# ==========================================
# GET API - Fetch Employees
@app.route("/fetch", methods=["GET"])
def fetch_employee():
    # MongoDB query object
    query = {}

    # Filter by employee ID
    if request.args.get("id"):
        query["id"] = int(request.args.get("id"))
        
    # Case-insensitive location search
    if request.args.get("work_location"):
        query["work_location"] = {
            "$regex": request.args.get("work_location"),
            "$options": "i"
        }
    
    # Salary range filter
    salary_query = {}

    #Minimum salary filter
    
    if request.args.get("salary_min"):
        salary_query["$gte"] = int(
            request.args.get("salary_min")
        )

    #Maximum salary filter
    if request.args.get("salary_max"):
        salary_query["$lte"] = int(
            request.args.get("salary_max")
        )

    #Add salary condition to main query if any salary filter is applied
    if salary_query:
        query["present_salary"] = salary_query

    if request.args.get("expected_hike"):
        query["expected_hike"] = int(
            request.args.get("expected_hike")
        )

    if request.args.get("performance_rating"):
        query["performance_rating"] = float(
            request.args.get("performance_rating")
        )

    if request.args.get("role"):
        query["role"] = {
            "$regex": request.args.get("role"),
            "$options": "i"
        }
    print("QUERY =", query)
    #fetch employees based on query
    employees = list(
        collection.find(
            query,
            {"_id": 0}
        )
    )
    
    #retuen json response
    return jsonify(employees)





# Assign  - Assign Employees to Project
@app.route("/assign", methods=["GET"])
def assign():
    rating = float(request.args.get("rating", 4))
    hike = float(request.args.get("hike", 20))
    role = request.args.get("role")

    query = {
        "performance_rating": {"$gte": rating},
        "expected_hike": {"$lte": hike}
    }

    if role:
        query["role"] = role

    employees = list(
        collection.find(query, {"_id": 0})
    )

    assigned_employees = []
    
    for emp in employees:

        rating = emp.get(
            "performance_rating",
        0
    )

        role = emp.get(
            "role",
        ""
    ).lower()

    # Main Project Assignment based on performance rating
    if rating >= 4.5:

        emp["assigned_project"] = (
            "Project Platinum"
        )

    elif rating >= 4.0:

        emp["assigned_project"] = (
            "Project Gold"
        )

    else:

        emp["assigned_project"] = (
            "Project Silver"
        )

    # Sub Assignment
    if role == "developer":

        emp["assigned_team"] = (
            "Backend Team"
        )

    elif role == "qa":

        emp["assigned_team"] = (
            "Testing Team"
        )

    elif role == "designer":

        emp["assigned_team"] = (
            "UI/UX Team"
        )

    elif role == "devops":

        emp["assigned_team"] = (
            "Infrastructure Team"
        )

    else:

        emp["assigned_team"] = (
            "Support Team"
        )

    assigned_employees.append(emp)

 

    return jsonify({
        "selected_count": len(assigned_employees),
        "employees": assigned_employees
    })




#verify data in mongodb
@app.route("/test")
def test():
    employees = list(collection.find({}, {"_id": 0})
    )
    return jsonify(employees)




#data upload from csv
@app.route("/upload-csv", methods=["POST"])
def upload_csv():

    print("FILES RECEIVED:", request.files)

    if "file" not in request.files:
        return jsonify({
            "error": "No file received",
            "received_keys": list(request.files.keys())
        }), 400

    file = request.files["file"]

    

    df = pd.read_csv(file)

    # Remove accidental header rows inside data
    df = df[df["id"] != "id"]

    # Convert columns
    df["id"] = pd.to_numeric(df["id"])

    df["present_salary"] = pd.to_numeric(
        df["present_salary"]
    )

    df["expected_hike"] = pd.to_numeric(
        df["expected_hike"]
    )

    df["performance_rating"] = pd.to_numeric(
        df["performance_rating"]
    )

    df["present_salary"] = (
        df["present_salary"].astype(int)
    )

    df["expected_hike"] = (
        df["expected_hike"].astype(int)
    )

    df["performance_rating"] = (
        df["performance_rating"].astype(float)
    )

    csv_count = len(df)

    employees = df.to_dict("records")

    collection.insert_many(employees)

    db_count = collection.count_documents({})

    return jsonify({
        "message": "CSV Uploaded Successfully",
        "csv_records": csv_count,
        "database_records": db_count
    })



# Employee Count API
@app.route("/employee-count", methods=["GET"])
def employee_count():
    count = collection.count_documents({})
    return jsonify({"total_employees": count})



#salary distribution API
@app.route("/salary-stats", methods=["GET"])
def salary_stats():

    pipeline = [
        {
            "$group": {
                "_id": None,
                "average_salary": {"$avg": "$present_salary"},
                "max_salary": {"$max": "$present_salary"},
                "min_salary": {"$min": "$present_salary"}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))

    return jsonify(result)



#clear database
@app.route("/clear-database", methods=["GET","DELETE"])
def clear_database():

    result = collection.delete_many({})

    return jsonify({
        "message": "Database cleared successfully",
        "deleted_count": result.deleted_count
    })

# ==========================================
# DELETE EMPLOYEE
# ==========================================

@app.route("/employee/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):

    result = collection.delete_one(
        {"id": emp_id}
    )

    if result.deleted_count == 0:

        return jsonify({
            "message":
            "Employee not found"
        }), 404

    create_audit_log(
        "DELETE",
        emp_id,
        "Employee deleted"
    )

    return jsonify({
        "message":
        "Employee deleted successfully"
    })

# ==========================================
# DYNAMIC FILTER APIs
#
# Purpose:
# Populate frontend dropdowns dynamically
# from MongoDB instead of hardcoding values.
#
# Benefits:
# 1. New locations automatically appear
# 2. New roles automatically appear
# 3. New hike values automatically appear
# 4. New ratings automatically appear
# 5. No need to modify HTML whenever
#    employee data changes
# ==========================================


# Fetch all unique work locations
# Used to populate Location dropdown
@app.route("/locations")
def get_locations():

    locations = collection.distinct(
        "work_location"
    )

    return jsonify(
        sorted(locations)
    )


# Fetch all unique employee roles
# Used to populate Role dropdown
@app.route("/roles")
def get_roles():

    roles = collection.distinct(
        "role"
    )

    return jsonify(
        sorted(roles)
    )


# Fetch all unique expected hike values
# Used to populate Hike dropdown
@app.route("/hikes")
def get_hikes():

    hikes = collection.distinct(
        "expected_hike"
    )

    hikes = [
        h for h in hikes
        if h is not None
    ]

    return jsonify(
        sorted(hikes)
    )

# Fetch all unique performance ratings
# Used to populate Rating dropdown
@app.route("/ratings")
def get_ratings():

    ratings = collection.distinct(
        "performance_rating"
    )

    ratings = [
        r for r in ratings
        if r is not None
    ]

    return jsonify(
        sorted(ratings)
    )


# ==========================================
# EXPORT FILTERED EMPLOYEES TO CSV
#
# Purpose:
# Download employee data matching
# selected filters as a CSV file.
#
# Why:
# HR users can export employee reports
# and open them in Excel.
# ==========================================

@app.route("/export-csv")
def export_csv():

    # MongoDB query object
    query = {} #Stores filters selected by the user.

    # Filter by location
    if request.args.get("work_location"):

        query["work_location"] = {
            "$regex": request.args.get(
                "work_location"
            ),
            "$options": "i"
        }

    # Filter by role
    if request.args.get("role"):

        query["role"] = {
            "$regex": request.args.get(
                "role"
            ),
            "$options": "i"
        }

    # Fetch matching employees
    employees = list(
        collection.find(  #Fetches only matching employees from MongoDB.
            query,
            {"_id": 0}
        )
    )

    # CSV file name
    file_name = "filtered_employees.csv"

    # Create CSV file
    with open(
        file_name,
        "w",
        newline=""
    ) as file:

        # Write only if employees exist
        if employees:

            writer = csv.DictWriter(
                file,
                fieldnames=
                employees[0].keys() #Gets column names automatically:
            )

            # Write column names
            writer.writeheader() #Creates CSV header row.

            # Write employee records
            writer.writerows( #Writes all employee records.
                employees
            )

    # Return downloadable file
    return send_file( #Makes browser download the generated CSV.
        file_name,
        as_attachment=True
    )

@app.route("/audit-logs")
def audit_logs():
    logs = list(
        audit_collection.find(
            {},
            {"_id":0}
        )
        .sort("timestamp",-1)
    )
    return jsonify(logs)


if __name__ == "__main__":
    app.run(debug=True)