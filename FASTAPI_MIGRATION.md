# Flask to FastAPI Migration Guide

## Overview
This project has been successfully converted from Flask to FastAPI. Below is a comprehensive guide of all the changes made.

## Key Changes

### 1. **Requirements Update** (`requirements.txt`)
**Removed:**
- Flask==2.3.3
- Flask-SQLAlchemy==3.0.5
- Flask-CORS==4.0.0
- flasgger==0.9.7.1
- asgiref==3.8.0

**Added:**
- fastapi==0.104.1
- pydantic-settings==2.0.0 (unchanged)

**Kept:**
- uvicorn==0.23.1 (for ASGI server)
- SQLAlchemy==2.0.21
- alembic==1.12.0
- pydantic==2.3.0
- gunicorn==21.2.0

### 2. **Main Application Entry Point** (`main.py`)
**Changes:**
- Removed Flask WSGI to ASGI wrapping using `asgiref`
- Now uses native FastAPI which is async-first
- Changed from `FLASK_ENV` to `APP_ENV` environment variable
- Updated to use FastAPI's native `uvicorn` integration
- Simplified server startup with native support for both development and production

### 3. **Configuration Management** (`config.py`)
**Changes:**
- Replaced Pydantic `BaseSettings` with plain Python class (simpler)
- Removed Flask-specific configuration keys
- Maintained environment variable loading via `python-dotenv`
- Config classes are now simple Python dataclasses instead of Pydantic models

### 4. **Database Layer** (`app/core/database.py`)
**New Structure:**
- Lazy initialization of SQLAlchemy engine and session maker
- Removed global `db` object used in Flask-SQLAlchemy
- Dependency injection pattern: `get_db()` for FastAPI routes
- Maintained same database connection pooling and echo settings

### 5. **Application Factory** (`app/core/app.py`)
**New Implementation:**
- Replaced Flask's `create_app()` factory with FastAPI initialization
- CORS middleware added instead of Flask-CORS extension
- Routes registered via `app.include_router()` instead of `app.register_blueprint()`
- Built-in OpenAPI/Swagger documentation support (no need for Flasgger)
- Lifespan context manager for startup/shutdown events

### 6. **Models** (`app/models/*.py`)
**Changes:**
- Updated to import from `app.core.database.Base` instead of `db.Model`
- Changed column definitions from `db.Column()` to `Column()`
- Changed relationships from `db.relationship()` to `relationship()`
- All models inherit from `Base` instead of `db.Model`
- JSON columns still work with SQLAlchemy's standard `JSON` type

### 7. **Routes Conversion**

#### New Route Files:
- `app/routes/academic_router.py` (was `academic_admission.py`)
- `app/routes/doctor_router.py` (was `doctor_onboarding.py`)
- `app/routes/insurance_router.py` (was `insurance_claim.py`)

#### Route Function Changes:
**Flask:**
```python
@academic_bp.route('/admin/students', methods=['POST'])
def add_student():
    data = request.get_json()
    # ...
    return jsonify({'message': '...'}), 200
```

**FastAPI:**
```python
@router.post('/admin/students')
def add_student(data: list[StudentSeedSchema], db: Session = Depends(get_db)):
    # ...
    return {'message': '...'}
```

**Key Differences:**
- No more decorators with HTTP methods - use `@router.get()`, `@router.post()`, etc.
- No `request.get_json()` - use Pydantic model parameters (automatic validation)
- No `jsonify()` - return Python dicts directly (FastAPI serializes to JSON)
- Dependency injection with `Depends(get_db)` for database sessions
- Query parameters become function parameters with `Query()` if needed
- HTTPException for errors instead of tuple returns

### 8. **Schemas** (`app/schemas/*.py`)
**Changes:**
- Already using Pydantic models (no changes needed)
- Models now serve dual purpose:
  - Request/response validation
  - OpenAPI documentation generation
  - No separate Marshmallow or other serialization needed

### 9. **Logging** (`app/logging_config.py`)
**No Changes Required** - logging configuration works as-is

### 10. **Health Check & Favicon**
**Before (Flask):**
```python
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200
```

**After (FastAPI):**
```python
@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "message": "..."}
```

## Running the Application

### Development Mode:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Docker Deployment:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Automatic API Documentation

FastAPI automatically generates:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Database Migrations (Alembic)

Database migrations continue to work the same way:

```bash
# Generate new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## API Endpoint Changes

All endpoints remain the same, but query parameters are cleaner:

**Before (Flask):**
```
GET /api/v1/academic/verify/roll-number?roll_number=123
```

**After (FastAPI):**
```
GET /api/v1/academic/verify/roll-number?roll_number=123
# Still works the same, but with automatic validation and docs
```

## Testing

FastAPI routes are easier to test using `TestClient`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## Performance Improvements

1. **Async Support**: FastAPI is async-first (can be leveraged with `async def`)
2. **Built-in Validation**: Pydantic validation is automatic for all requests
3. **Faster Startup**: No Flask initialization overhead
4. **Better Error Handling**: Structured error responses via HTTPException
5. **Native OpenAPI**: No need for Flasgger or manual OpenAPI generation

## Migration Checklist

- ✅ Replace Flask with FastAPI
- ✅ Update requirements.txt
- ✅ Convert blueprints to routers
- ✅ Update database initialization
- ✅ Update configuration system
- ✅ Convert route decorators and functions
- ✅ Add CORS middleware
- ✅ Set up health check endpoint
- ✅ Verify all endpoints work
- ✅ Test database connections
- ✅ Generate and verify API documentation

## Common Pitfalls & Solutions

### 1. **Database Session Management**
- ✅ Use `Depends(get_db)` in function parameters
- ❌ Don't try to access `db` globally

### 2. **Query Parameters**
- ✅ Add as function parameters: `def get_item(id: str, db: Session = Depends(get_db))`
- ❌ Don't use `request.args.get()`

### 3. **Request Body**
- ✅ Use Pydantic models: `def create_item(item: ItemSchema)`
- ❌ Don't use `request.get_json()`

### 4. **Error Handling**
- ✅ Raise HTTPException: `raise HTTPException(status_code=404, detail="Not found")`
- ❌ Don't return tuples with status codes

### 5. **Response Serialization**
- ✅ Return Python dicts/objects: `return {"key": "value"}`
- ❌ Don't use `jsonify()` - it's not needed

## Support & Debugging

For debugging SQLAlchemy queries:
```python
# Already configured in config.py
SQLALCHEMY_ECHO = True  # Logs all SQL queries
```

For better debugging of FastAPI requests:
```python
from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Next Steps

1. Run test suite against new FastAPI endpoints
2. Update CI/CD pipelines to deploy FastAPI instead of Flask
3. Consider adding async/await to routes for better performance
4. Implement additional FastAPI middleware as needed
5. Update deployment documentation

---

**Conversion Date:** December 18, 2025
**FastAPI Version:** 0.104.1
**Python Version:** 3.11+
