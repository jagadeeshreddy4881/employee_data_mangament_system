from fastapi import APIRouter

dashboard_router = APIRouter()

# ==========================================
# EMPLOYEE COUNT
# ==========================================
@dashboard_router.get("/employee-count")
def employee_count():

    return {
        "message": "Employee Count API Working"
    }


# ==========================================
# SALARY STATS
# ==========================================
@dashboard_router.get("/salary-stats")
def salary_stats():

    return {
        "message": "Salary Stats API Working"
    }


# ==========================================
# LOCATIONS
# ==========================================
@dashboard_router.get("/locations")
def get_locations():

    return {
        "message": "Locations API Working"
    }


# ==========================================
# ROLES
# ==========================================
@dashboard_router.get("/roles")
def get_roles():

    return {
        "message": "Roles API Working"
    }


# ==========================================
# HIKES
# ==========================================
@dashboard_router.get("/hikes")
def get_hikes():

    return {
        "message": "Hikes API Working"
    }


# ==========================================
# RATINGS
# ==========================================
@dashboard_router.get("/ratings")
def get_ratings():

    return {
        "message": "Ratings API Working"
    }


# ==========================================
# EXPORT CSV
# ==========================================
@dashboard_router.get("/export-csv")
def export_csv():

    return {
        "message": "Export CSV API Working"
    }