from flask import (
    Blueprint,
    jsonify,
    request,
    send_file
)

import csv

from database.mongo import collection

# Blueprint for dashboard APIs
dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__
)

# ==========================================
# Employee Count API Endpoint
# ==========================================
@dashboard_bp.route("/employee-count", methods=["GET"])
def employee_count():
    count = collection.count_documents({})
    return jsonify({"total_employees": count})

# ==========================================
# Salary Distribution API Endpoint (average, max, min)
# ==========================================
@dashboard_bp.route("/salary-stats", methods=["GET"])
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

#=============================================
# locations endpoint: Fetches all unique work locations from the MongoDB collection and returns them as a sorted JSON list. 
# This is used to dynamically populate the Location dropdown in the frontend, ensuring that any new locations added to the database will automatically 
# appear in the dropdown without requiring changes to the HTML code.
#=============================================
@dashboard_bp.route("/locations")
def get_locations():

    locations = collection.distinct(
        "work_location"
    )

    return jsonify(
        sorted(locations)
    )

#=============================================
# roles endpoint: Fetches all unique employee roles from the MongoDB collection and 
# returns them as a sorted JSON list. This endpoint is used to dynamically 
# populate the Role dropdown in the frontend, allowing any new roles added to the database to 
# automatically appear in the dropdown without needing to modify the HTML code.
#=============================================
@dashboard_bp.route("/roles")
def get_roles():

    roles = collection.distinct(
        "role"
    )

    return jsonify(
        sorted(roles)
    )

#=============================================
# hikes endpoint: Fetches all unique expected hike values from the MongoDB collection and returns them
# as a sorted JSON list. This endpoint is used to dynamically populate the Hike dropdown in the frontend, 
# ensuring that any new hike values added to the database will automatically appear in the dropdown without requiring changes to the HTML code.
#=============================================
@dashboard_bp.route("/hikes")
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

#=============================================
# ratings endpoint: Fetches all unique performance ratings from the MongoDB collection and returns
#  them as a sorted JSON list. This endpoint is used to dynamically populate the Performance Rating dropdown in the frontend,
@dashboard_bp.route("/ratings")
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

#=============================================
# Export CSV Endpoint
# ==============================================
@dashboard_bp.route("/export-csv")
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
