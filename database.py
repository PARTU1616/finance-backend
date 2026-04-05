"""
Database instance module.
This module is imported by models to avoid circular imports.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
