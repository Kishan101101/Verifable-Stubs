#!/bin/bash

# Setup script for Verifiable Stubs API

echo "=========================================="
echo "Verifiable Stubs API - Setup Script"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env .env.example 2>/dev/null || echo "Note: .env file not found, creating default..."
    cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=verifiable_stubs

# Database URL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/verifiable_stubs

# API Configuration
API_TITLE=Verifiable Stubs APIs
API_VERSION=1.0.0
EOF
    echo ".env file created. Update credentials as needed."
fi

# Create database (optional)
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update .env file with your database credentials"
echo "2. Create PostgreSQL database: createdb -U postgres verifiable_stubs"
echo "3. Run migrations: python -m alembic upgrade head"
echo "4. Start the app: python run.py"
echo ""
echo "Swagger UI will be available at: http://localhost:5000/apidocs/"
echo ""
