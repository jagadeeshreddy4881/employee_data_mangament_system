from flask import (
    Blueprint,
    jsonify,
    request
)

import pandas as pd

from database.mongo import collection

from services.audit_service import (
    create_audit_log
)

# Blueprint for employee APIs
employee_bp = Blueprint(
    "employee_bp",
    __name__
)

# ==========================================
# Add EMPLOYEE
# ==========================================
@employee_bp.route("/employee", methods=["POST"])
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

# ==========================================
# Update EMPLOYEE
# ==========================================
@employee_bp.route("/employee/<int:emp_id>", methods=["PUT"])
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

# ==========================================
# DELETE EMPLOYEE
# ==========================================
@employee_bp.route("/employee/<int:emp_id>", methods=["DELETE"])
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
# ==========================================
@employee_bp.route("/fetch", methods=["GET"])
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

# ==========================================
# Assign  - Assign Employees to Project
# ==========================================
@employee_bp.route("/assign", methods=["GET"])
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

# ==========================================
#data upload from csv
# ==========================================
@employee_bp.route("/upload-csv", methods=["POST"])
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

# ==========================================
# Remove Duplicates - Remove duplicate employee records based on ID
# ==========================================
@employee_bp.route("/remove-duplicates")
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
# Clear Database - Remove all employee records from database
# ==========================================
@employee_bp.route("/clear-database", methods=["GET","DELETE"])
def clear_database():

    result = collection.delete_many({})

    return jsonify({
        "message": "Database cleared successfully",
        "deleted_count": result.deleted_count
    })

# ==========================================
# Test Route - Verify data in MongoDB and API connectivity 
#=========================================
@employee_bp.route("/test")
def test():
    employees = list(collection.find({}, {"_id": 0})
    )
    return jsonify(employees)

# ==========================================
# TEST UPDATE ROUTE
# ==========================================
@employee_bp.route("/test-update")
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