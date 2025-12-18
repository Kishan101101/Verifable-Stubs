@echo off
REM Setup script for Verifiable Stubs API (Windows)

echo ==========================================
echo Verifiable Stubs API - Setup Script
echo ==========================================

REM Check Python version
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Setup environment file
if not exist .env (
    echo Creating .env file...
    (
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
        echo SECRET_KEY=dev-secret-key-change-in-production
        echo.
        echo # Database Configuration
        echo DB_USER=postgres
        echo DB_PASSWORD=postgres
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo DB_NAME=verifiable_stubs
        echo.
        echo # Database URL
        echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/verifiable_stubs
        echo.
        echo # API Configuration
        echo API_TITLE=Verifiable Stubs APIs
        echo API_VERSION=1.0.0
    ) > .env
    echo .env file created. Update credentials as needed.
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Update .env file with your database credentials
echo 2. Create PostgreSQL database: createdb -U postgres verifiable_stubs
echo 3. Run migrations: python -m alembic upgrade head
echo 4. Start the app: python run.py
echo.
echo Swagger UI will be available at: http://localhost:5000/apidocs/
echo.
pause
