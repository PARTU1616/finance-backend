"""
Database initialization script.
Run this to create all tables in the database.

Usage:
    python init_db.py
"""
from app import app
from database import db
from models.user import User
from models.financial_record import FinancialRecord

with app.app_context():
    # Create all tables
    db.create_all()
    print("✓ Database tables created successfully!")
    
    # Create a default admin user if none exists
    admin = User.query.filter_by(email='admin@finance.com').first()
    if not admin:
        admin = User(
            email='admin@finance.com',
            role='Admin',
            status='active'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin user created (email: admin@finance.com, password: admin123)")
    else:
        print("✓ Admin user already exists")
    
    print("\nDatabase initialization complete!")
