from database import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Viewer, Analyst, Admin
    status = db.Column(db.String(50), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    financial_records = db.relationship('FinancialRecord', foreign_keys='FinancialRecord.created_by', backref='creator', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by
        }
    
    def set_password(self, password):
        """Hash and set password using bcrypt."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
