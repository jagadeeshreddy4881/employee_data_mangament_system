from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_file
)

import pandas as pd
import csv

from database.mongo import (
    collection,
    audit_collection
)

from services.audit_service import (
    create_audit_log
)from database.mongo import (
    collection,
    audit_collection
)

from services.audit_service import (
    create_audit_log
)





from routes.system_routes import system_bp
from routes.employee_routes import employee_bp
from routes.dashboards_routes import dashboard_bp
from routes.audit_routes import audit_bp
# ==========================================
# CREATE FLASK APPLICATION
# ==========================================
app = Flask(__name__)

app.register_blueprint(system_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(audit_bp)
