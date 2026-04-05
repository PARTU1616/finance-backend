from database import db
from datetime import datetime

class FinancialRecord(db.Model):
    __tablename__ = 'financial_records'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # income, expense
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'type': self.type,
            'category': self.category,
            'date': self.date.isoformat() if self.date else None,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_by': self.updated_by,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
