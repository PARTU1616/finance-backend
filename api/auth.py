from flask import Blueprint, request, session, jsonify
from models.user import User
from database import db
from utils.authorization import requires_auth

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login/', methods=['POST'])
def login():
    """
    Authenticate user and create session.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    
    Response:
        200: {ok: true, data: {user_id, email, role}, msg: "Login successful"}
        401: {ok: false, error: "Invalid credentials"}
    """
    data = request.json
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify(ok=False, error="Missing email or password", msg="Email and password are required"), 400
    
    email = data.get('email').lower()
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify(ok=False, error="Invalid credentials", msg="Invalid email or password"), 401
    
    if user.status != 'active':
        return jsonify(ok=False, error="Account inactive", msg="Your account has been deactivated"), 401
    
    # Create session
    session['user_id'] = user.id
    session['email'] = user.email
    session['role'] = user.role
    
    return jsonify(
        ok=True,
        data={
            'user_id': user.id,
            'email': user.email,
            'role': user.role
        },
        msg="Login successful"
    ), 200

@auth_bp.route('/logout/', methods=['POST'])
@requires_auth()
def logout():
    """
    Destroy user session.
    
    Response:
        200: {ok: true, msg: "Logged out successfully"}
    """
    session.clear()
    return jsonify(ok=True, msg="Logged out successfully"), 200

@auth_bp.route('/session/', methods=['GET'])
@requires_auth()
def get_session():
    """
    Get current session information.
    
    Response:
        200: {ok: true, data: {user_id, email, role}}
    """
    return jsonify(
        ok=True,
        data={
            'user_id': session.get('user_id'),
            'email': session.get('email'),
            'role': session.get('role')
        },
        msg="Session retrieved"
    ), 200
