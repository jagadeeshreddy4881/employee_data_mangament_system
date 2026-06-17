# ==========================================
# FLASK IMPORTS
# ==========================================

from flask import (
    Flask,
    render_template
)
# ==========================================
#import Blue prints
# ==========================================
from routes.system_routes import system_bp
from routes.employee_routes import employee_bp
from routes.dashboards_routes import dashboard_bp
from routes.audit_routes import audit_bp
# ==========================================
# CREATE FLASK APPLICATION
# ==========================================
app = Flask(__name__)

# ==========================================
# REGISTER BLUEPRINTS
# Registers all application modules
# with the Flask application.
# ==========================================

# System APIs
app.register_blueprint(system_bp)
# Employee APIs
app.register_blueprint(employee_bp)
# Dashboard APIs
app.register_blueprint(dashboard_bp)
# Audit APIs
app.register_blueprint(audit_bp)

# ==========================================
# HOME PAGE
# Purpose:
# Load Employee Management System UI
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )