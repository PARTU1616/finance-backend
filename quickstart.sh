#!/bin/bash

# Finance Backend Quick Start Script
# This script helps you get the backend up and running quickly

echo "🚀 Finance Backend Quick Start"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

echo "✓ Python 3 found"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL 12+ and create a database named 'finance_db'"
    echo "   On Ubuntu/Debian: sudo apt-get install postgresql"
    echo "   On macOS: brew install postgresql"
else
    echo "✓ PostgreSQL found"
fi

# Check if Redis is installed
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis not found. Please install Redis 6+"
    echo "   On Ubuntu/Debian: sudo apt-get install redis-server"
    echo "   On macOS: brew install redis"
else
    echo "✓ Redis found"
fi

echo ""
echo "📦 Setting up virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "🗄️  Setting up database..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your settings."
fi

# Initialize database
echo "Initializing database tables and creating admin user..."
python init_db.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Edit .env file with your database and Redis settings"
echo "   2. Run: python app.py"
echo "   3. Test: python test_api.py"
echo "   4. Login with: admin@finance.com / admin123"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Setup and usage guide"
echo "   - API_DOCUMENTATION.md - Complete API reference"
echo "   - PROJECT_SUMMARY.md - Project overview"
echo ""
echo "Happy coding! 🎉"
