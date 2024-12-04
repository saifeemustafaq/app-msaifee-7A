from ..extensions import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    academic_program = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text)
    linkedin_url = db.Column(db.String(255))
    language_preferences = db.Column(db.String(255))
    cultural_background = db.Column(db.String(255)) 