from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..extensions import db
from ..utils.decorators import admin_required
from ..utils.pagination import paginate

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get all users with pagination"""
    return paginate(User.query)

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get a specific user by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update a user's information"""
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Only allow users to update their own profile unless they're an admin
    if current_user_id != user.id and not User.query.get(current_user_id).is_admin:
        return jsonify({'message': 'Unauthorized'}), 403
        
    data = request.get_json()
    
    try:
        # Update allowed fields
        allowed_fields = ['email', 'username', 'first_name', 'last_name', 
                         'phone_number', 'campus_affiliation']
        
        for field in allowed_fields:
            if field in data:
                # Check uniqueness for email and username
                if field == 'email' and data['email'] != user.email:
                    if User.query.filter_by(email=data['email']).first():
                        return jsonify({'message': 'Email already exists'}), 400
                elif field == 'username' and data['username'] != user.username:
                    if User.query.filter_by(username=data['username']).first():
                        return jsonify({'message': 'Username already exists'}), 400
                setattr(user, field, data[field])
        
        # Handle password update separately if provided
        if 'password' in data:
            user.set_password(data['password'])
        
        db.session.commit()
        return jsonify(user.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@user_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'first_name', 
                      'last_name', 'phone_number', 'campus_affiliation']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            campus_affiliation=data['campus_affiliation'],
            token_balance=0  # Initialize token balance to 0
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400