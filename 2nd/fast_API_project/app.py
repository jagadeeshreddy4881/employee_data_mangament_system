# ==========================================
# FASTAPI IMPORTS
# ==========================================

# FastAPI -> Creates the web application

from sys import audit

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from database.mongo import collection
from routes.system_routes import system_router
from routes.employee_routes import employee_router
from routes.dashboard_routes import dashboard_router
from routes.audit_routes import audit_router
# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================
#in flask project, we are using Flask(__name__)

app = FastAPI()


#===========================================
#
#===========================================
app.include_router(system_router)
app.include_router(employee_router)
app.include_router(dashboard_router)
app.include_router(audit_router)


# ==========================================
# LOAD HTML TEMPLATES
# ==========================================

templates = Jinja2Templates(
    directory="templates"
)

# ==========================================
# HOME API
#
# Purpose:
# Verify FastAPI is running
# ==========================================
#in Flask (we use route inside that we will mention methods like (get, put etc..))
#in Fastapi we use .get, .put, .post etc...
#Each HTTP method has its own decorator.

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

# ==========================================
# HEALTH CHECK API
#
# Purpose:
# Verify FastAPI server is running
# ==========================================

@app.get("/health")
def API_health_check():

    return {
        "status": "Success",
        "message": "FastAPI is running"
    }
