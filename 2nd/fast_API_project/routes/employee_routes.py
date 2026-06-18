from fastapi import APIRouter

employee_router = APIRouter()

# ==========================================
# ADD EMPLOYEE
# ==========================================
@employee_router.post("/employee")
def add_employee():

    return {
        "message": "Add Employee API Working"
    }


# ==========================================
# UPDATE EMPLOYEE
# ==========================================
@employee_router.put("/employee/{emp_id}")
def update_employee(emp_id: int):

    return {
        "message": "Update Employee API Working",
        "employee_id": emp_id
    }


# ==========================================
# DELETE EMPLOYEE
# ==========================================
@employee_router.delete("/employee/{emp_id}")
def delete_employee(emp_id: int):

    return {
        "message": "Delete Employee API Working",
        "employee_id": emp_id
    }


# ==========================================
# FETCH EMPLOYEES
# ==========================================
@employee_router.get("/fetch")
def fetch_employees():

    return {
        "message": "Fetch Employees API Working"
    }


# ==========================================
# ASSIGN EMPLOYEES
# ==========================================
@employee_router.get("/assign")
def assign_employees():

    return {
        "message": "Assign Employees API Working"
    }


# ==========================================
# UPLOAD CSV
# ==========================================
@employee_router.post("/upload-csv")
def upload_csv():

    return {
        "message": "Upload CSV API Working"
    }


# ==========================================
# REMOVE DUPLICATES
# ==========================================
@employee_router.get("/remove-duplicates")
def remove_duplicates():

    return {
        "message": "Remove Duplicates API Working"
    }


# ==========================================
# CLEAR DATABASE
# ==========================================
@employee_router.api_route(
    "/clear-database",
    methods=["GET", "DELETE"]
)
def clear_database():

    return {
        "message": "Clear Database API Working"
    }


# ==========================================
# TEST API
# ==========================================
@employee_router.get("/test")
def test():

    return {
        "message": "Test API Working"
    }


# ==========================================
# TEST UPDATE API
# ==========================================
@employee_router.get("/test-update")
def test_update():

    return {
        "message": "Test Update API Working"
    }