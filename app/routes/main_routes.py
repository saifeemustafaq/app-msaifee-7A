from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """Root endpoint that returns API information"""
    return jsonify({
        'name': 'Student Token Management API',
        'version': '1.0',
        'documentation': '/docs',
        'status': 'operational'
    }) 