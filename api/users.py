from flask import Blueprint, request, jsonify, session
from models.user import User
from database import db
from utils.authorization import requires_auth

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/list/', methods=['GET'])
@requires_auth(roles=['Admin'])
def list_users():
    """List users with pagination and search."""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '').strip()
    
    query = User.query
    
    if search:
        query = query.filter(User.email.ilike(f'%{search}%'))
    
    total_count = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()
    
    return jsonify(
        ok=True,
        users=[user.to_dict() for user in users],
        total_count=total_count,
        msg="Success"
    ), 200

@users_bp.route('/create/', methods=['POST'])
@requires_auth(roles=['Admin'])
def create_user():
    """Create user."""
    data = request.json
    
    if not data:
        return jsonify(ok=False, msg="No data"), 400
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not email or not password or not role:
        return jsonify(ok=False, msg="Missing fields"), 400
    
    if role not in ['Viewer', 'Analyst', 'Admin']:
        return jsonify(ok=False, msg="Invalid role"), 400
    
    if User.query.filter_by(email=email.lower()).first():
        return jsonify(ok=False, msg="Email exists"), 400
    
    user = User(
        email=email.lower(), 
        role=role, 
        status='active',
        created_by=session.get('user_id')
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(ok=True, data=user.to_dict(), msg="Success"), 200

@users_bp.route('/update/<int:user_id>/', methods=['POST'])
@requires_auth(roles=['Admin'])
def update_user(user_id):
    """Update user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify(ok=False, msg="Not found"), 404
    
    data = request.json
    if not data:
        return jsonify(ok=False, msg="No data"), 400
    
    if 'email' in data:
        email = data['email'].lower()
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify(ok=False, msg="Email exists"), 400
        user.email = email
    
    if 'role' in data:
        if data['role'] not in ['Viewer', 'Analyst', 'Admin']:
            return jsonify(ok=False, msg="Invalid role"), 400
        user.role = data['role']
    
    user.updated_by = session.get('user_id')
    db.session.commit()
    return jsonify(ok=True, data=user.to_dict(), msg="Success"), 200

@users_bp.route('/deactivate/<int:user_id>/', methods=['POST'])
@requires_auth(roles=['Admin'])
def deactivate_user(user_id):
    """Deactivate user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify(ok=False, msg="Not found"), 404
    
    user.status = 'inactive'
    user.updated_by = session.get('user_id')
    db.session.commit()
    return jsonify(ok=True, msg="Success"), 200
