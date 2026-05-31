from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]
print("MongoDB Connected Successfully")

#dbtest
@app.route("/dbtest")
def dbtest():
    try:
        collection.count_documents({})
        return "MongoDB Connected"
    except Exception as e:
        return str(e)
    

#check connection
@app.route("/hello")
def hello():
    return "Hello jagadeesh"


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



# GET API - Fetch Employees
@app.route("/fetch", methods=["GET"])

def fetch_employee():

    query = {}

    if request.args.get("id"):
        query["id"] = int(request.args.get("id"))

    if request.args.get("work_location"):
        query["work_location"] = {
            "$regex": request.args.get("work_location"),
            "$options": "i"
        }

    if request.args.get("salary"):
        query["present_salary"] = int(
            request.args.get("salary")
        )

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

    employees = list(
        collection.find(
            query,
            {"_id": 0}
        )
    )

    return jsonify(employees)


# Aggregate API - Assign Employees to Project
@app.route("/aggregate", methods=["GET"])
def aggregate():

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
        emp["assigned_project"] = "Project Phoenix"
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


if __name__ == "__main__":
    app.run(debug=True)



