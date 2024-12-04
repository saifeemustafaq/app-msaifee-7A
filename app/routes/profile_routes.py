from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.profile import UserProfile
from ..extensions import db
from ..utils.pagination import paginate
from ..utils.decorators import admin_required

profile_bp = Blueprint('profile', __name__, url_prefix='/profiles')

@profile_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def get_profiles():
    """Get all profiles with pagination"""
    return paginate(UserProfile.query)

@profile_bp.route('/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    """Get a specific profile"""
    profile = UserProfile.query.get_or_404(profile_id)
    return jsonify(profile.to_dict())

@profile_bp.route('/', methods=['POST'])
@jwt_required()
def create_profile():
    """Create a new profile"""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Check if profile already exists
    existing_profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    if existing_profile:
        return jsonify({'message': 'Profile already exists'}), 400
        
    # Validate required fields
    required_fields = ['academic_program', 'graduation_year']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    try:
        profile = UserProfile(
            user_id=current_user_id,
            academic_program=data['academic_program'],
            graduation_year=data['graduation_year'],
            bio=data.get('bio'),
            linkedin_url=data.get('linkedin_url'),
            language_preferences=data.get('language_preferences'),
            cultural_background=data.get('cultural_background')
        )
        
        db.session.add(profile)
        db.session.commit()
        return jsonify(profile.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@profile_bp.route('/<int:profile_id>', methods=['PUT'])
@jwt_required()
def update_profile(profile_id):
    """Update a profile"""
    current_user_id = get_jwt_identity()
    profile = UserProfile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    for field in ['academic_program', 'graduation_year', 'bio', 'linkedin_url', 
                 'language_preferences', 'cultural_background']:
        if field in data:
            setattr(profile, field, data[field])
    
    try:
        db.session.commit()
        return jsonify(profile.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

@profile_bp.route('/<int:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_profile(profile_id):
    """Delete a profile"""
    current_user_id = get_jwt_identity()
    profile = UserProfile.query.get_or_404(profile_id)
    
    if profile.user_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403
        
    try:
        db.session.delete(profile)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400