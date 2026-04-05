import os
import decimal
import datetime
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from json import JSONEncoder
import redis
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)

# CORS
CORS(app, supports_credentials=True, origins=app.config['CORS_ORIGINS'], allow_headers=['Content-Type'], expose_headers=['Set-Cookie'])

# Redis session
redis_client = redis.from_url(app.config['SESSION_REDIS_URL'])
app.config['SESSION_REDIS'] = redis_client
Session(app)

# Database
db.init_app(app)
migrate = Migrate(app, db)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['SESSION_REDIS_URL']
)

# JSON encoder
class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = JsonEncoder

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify(
        ok=False,
        error="Bad Request",
        msg="The request could not be understood or was missing required parameters"
    ), 400

@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized errors"""
    return jsonify(
        ok=False,
        error="Unauthorized",
        msg="Authentication is required to access this resource"
    ), 401

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors"""
    return jsonify(
        ok=False,
        error="Forbidden",
        msg="You do not have permission to access this resource"
    ), 403

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify(
        ok=False,
        error="Not Found",
        msg="The requested resource could not be found"
    ), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    db.session.rollback()
    return jsonify(
        ok=False,
        error="Internal Server Error",
        msg="An unexpected error occurred. Please try again later"
    ), 500

# Register blueprints
from api.auth import auth_bp
from api.users import users_bp
from api.transactions import transactions_bp
from api.dashboard import dashboard_bp
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    try:
        return jsonify(ok=True, msg="Finance Backend API is running", version="1.0.0")
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

@app.route('/init-db')
def init_database():
    """Initialize database tables and create default admin user (one-time use)"""
    try:
        from models.user import User
        from models.financial_record import FinancialRecord
        
        # Create tables
        db.create_all()
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@finance.com').first()
        if admin:
            return jsonify(ok=False, msg="Database already initialized")
        
        # Create default admin user
        admin = User(
            email='admin@finance.com',
            role='Admin',
            status='active'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        return jsonify(ok=True, msg="Database initialized successfully! Default admin: admin@finance.com / admin123")
    except Exception as e:
        db.session.rollback()
        return jsonify(ok=False, error=str(e), msg="Failed to initialize database"), 500

if __name__ == '__main__':
    app.run(debug=True)
