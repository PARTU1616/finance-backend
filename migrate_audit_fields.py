"""
Migration script to add audit fields (created_by, updated_by) to tables.
Run this once to update existing database schema.
"""
from app import app
from database import db

with app.app_context():
    # Add columns using raw SQL
    with db.engine.connect() as conn:
        # Add created_by and updated_by to users table
        try:
            conn.execute(db.text('ALTER TABLE users ADD COLUMN created_by INTEGER REFERENCES users(id)'))
            print("✓ Added created_by to users table")
        except Exception as e:
            print(f"  created_by already exists in users: {e}")
        
        try:
            conn.execute(db.text('ALTER TABLE users ADD COLUMN updated_by INTEGER REFERENCES users(id)'))
            print("✓ Added updated_by to users table")
        except Exception as e:
            print(f"  updated_by already exists in users: {e}")
        
        # Add updated_by to financial_records table
        try:
            conn.execute(db.text('ALTER TABLE financial_records ADD COLUMN updated_by INTEGER REFERENCES users(id)'))
            print("✓ Added updated_by to financial_records table")
        except Exception as e:
            print(f"  updated_by already exists in financial_records: {e}")
        
        conn.commit()
    
    print("\n✓ Migration complete! Audit fields added to all tables.")
