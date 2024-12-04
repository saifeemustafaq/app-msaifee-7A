from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.activity import TokenActivity
from ..models.user import User
from ..extensions import db
from ..utils.decorators import admin_required
from ..utils.pagination import paginate

activity_bp = Blueprint('activity', __name__, url_prefix='/activities')

@activity_bp.route('/', methods=['GET'])
@jwt_required()
def get_activities():
    """Get all activities for current user"""
    current_user_id = get_jwt_identity()
    activities = TokenActivity.query.filter_by(user_id=current_user_id)
    return paginate(activities)

@activity_bp.route('/<int:activity_id>', methods=['GET'])
@jwt_required()
def get_activity(activity_id):
    """Get a specific activity"""
    current_user_id = get_jwt_identity()
    activity = TokenActivity.query.filter_by(
        activity_id=activity_id, 
        user_id=current_user_id
    ).first_or_404()
    return jsonify(activity.to_dict())

@activity_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_activity():
    """Create a new activity"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_id', 'activity_type', 'amount', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
            
    # Validate activity type
    if data['activity_type'] not in ['CREDIT', 'DEBIT']:
        return jsonify({'message': 'Invalid activity type'}), 400
        
    user = User.query.get_or_404(data['user_id'])
    
    activity = TokenActivity(
        user_id=data['user_id'],
        activity_type=data['activity_type'],
        amount=data['amount'],
        description=data['description']
    )
    
    try:
        # Update user's token balance
        if data['activity_type'] == 'CREDIT':
            user.token_balance += data['amount']
        elif data['activity_type'] == 'DEBIT':
            if user.token_balance < data['amount']:
                return jsonify({'message': 'Insufficient tokens'}), 400
            user.token_balance -= data['amount']
        
        db.session.add(activity)
        db.session.commit()
        return jsonify(activity.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@activity_bp.route('/<int:activity_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_activity(activity_id):
    """Delete an activity"""
    activity = TokenActivity.query.get_or_404(activity_id)
    user = User.query.get(activity.user_id)
    
    try:
        # Revert the token balance change
        if activity.activity_type == 'CREDIT':
            if user.token_balance < activity.amount:
                return jsonify({'message': 'Cannot delete - insufficient tokens'}), 400
            user.token_balance -= activity.amount
        elif activity.activity_type == 'DEBIT':
            user.token_balance += activity.amount
            
        db.session.delete(activity)
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400