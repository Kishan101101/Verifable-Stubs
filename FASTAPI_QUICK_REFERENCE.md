# FastAPI Quick Reference for This Project

## Project Structure

```
Verifable-Stubs/
├── main.py                          # Entry point
├── config.py                        # Configuration management
├── requirements.txt                 # Dependencies
├── alembic.ini                      # Database migration config
├── app/
│   ├── __init__.py                  # Package marker
│   ├── core/
│   │   ├── __init__.py
│   │   ├── app.py                   # FastAPI app factory
│   │   └── database.py              # SQLAlchemy setup & session management
│   ├── models/                      # SQLAlchemy ORM models
│   │   ├── academic.py
│   │   ├── doctor.py
│   │   └── insurance.py
│   ├── routes/                      # API route handlers
│   │   ├── academic_router.py
│   │   ├── doctor_router.py
│   │   └── insurance_router.py
│   ├── schemas/                     # Pydantic request/response schemas
│   │   ├── academic_schema.py
│   │   ├── doctor_schema.py
│   │   └── insurance_schema.py
│   └── logging_config.py            # Logging configuration
└── migrations/                      # Alembic database migrations
```

## Running the Application

### Development (with auto-reload):
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production (with Gunicorn):
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Access API Documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## Creating New Routes

### 1. Create a Router File
```python
# app/routes/my_router.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.mymodel import MyModel
from app.schemas.myschema import MySchema

router = APIRouter()

@router.post('/create')
def create_item(data: MySchema, db: Session = Depends(get_db)):
    """Create a new item"""
    try:
        item = MyModel(**data.dict())
        db.add(item)
        db.commit()
        db.refresh(item)
        return {'id': item.id, 'message': 'Item created'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/get/{item_id}')
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get an item by ID"""
    item = db.query(MyModel).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item.to_dict()
```

### 2. Register Router in main app
In `app/core/app.py`:
```python
from app.routes.my_router import router as my_router
# ...
app.include_router(my_router, prefix="/api/v1/myresource", tags=["MyResource"])
```

## Common API Patterns

### GET with Query Parameters
```python
@router.get('/search')
def search(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search for items"""
    items = db.query(MyModel).filter(...).limit(limit).all()
    return {'count': len(items), 'items': [i.to_dict() for i in items]}
```

### POST with JSON Body
```python
@router.post('/create')
def create(data: MySchema, db: Session = Depends(get_db)):
    """Create new item"""
    obj = MyModel(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {'id': obj.id, 'created': True}
```

### PUT/PATCH with Path Parameter
```python
@router.put('/update/{item_id}')
def update(item_id: int, data: MySchema, db: Session = Depends(get_db)):
    """Update an item"""
    item = db.query(MyModel).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Not found')
    for key, value in data.dict().items():
        setattr(item, key, value)
    db.commit()
    return {'updated': True, 'item': item.to_dict()}
```

### DELETE
```python
@router.delete('/delete/{item_id}')
def delete(item_id: int, db: Session = Depends(get_db)):
    """Delete an item"""
    item = db.query(MyModel).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Not found')
    db.delete(item)
    db.commit()
    return {'deleted': True}
```

## Request/Response Schemas

### Define Schemas
```python
# app/schemas/myschema.py
from pydantic import BaseModel
from typing import Optional

class MySchema(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class MyResponseSchema(BaseModel):
    id: int
    name: str
    created_at: str
```

### Usage in Routes
```python
@router.post('/create')
def create(item: MySchema) -> MyResponseSchema:  # Request & response type hints
    """Create with automatic validation and docs"""
    # MySchema validates the JSON body automatically
    # Response is automatically serialized to JSON
    return MyResponseSchema(id=1, name=item.name, created_at="2025-12-18")
```

## Error Handling

### Common HTTP Errors
```python
from fastapi import HTTPException

# 400 Bad Request
raise HTTPException(status_code=400, detail="Invalid input")

# 404 Not Found
raise HTTPException(status_code=404, detail="Item not found")

# 500 Internal Server Error
raise HTTPException(status_code=500, detail="Database error")

# Custom error response
raise HTTPException(
    status_code=422,
    detail={
        "error": "Validation failed",
        "fields": ["name", "email"]
    }
)
```

## Database Operations

### Query Examples
```python
from app.models.academic import StudentSeed

# Get single item
student = db.query(StudentSeed).filter_by(student_id="S001").first()

# Get multiple items
students = db.query(StudentSeed).filter(StudentSeed.marks > 80).all()

# Get with relationships
student = db.query(StudentSeed).filter_by(student_id="S001").first()
records = student.academic_records  # Access related data

# Aggregation
count = db.query(StudentSeed).count()
max_marks = db.query(StudentSeed).with_entities(func.max(StudentSeed.marks)).scalar()
```

### Create/Update/Delete
```python
# Create
new_student = StudentSeed(student_id="S002", name="John", dob="2000-01-01")
db.add(new_student)
db.commit()
db.refresh(new_student)

# Update
student.name = "Jane"
db.commit()

# Delete
db.delete(student)
db.commit()
```

## Pydantic Validation

### Schema Validation Examples
```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class StudentSchema(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    marks: float = Field(..., ge=0, le=100)  # Between 0 and 100
    email: Optional[str] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email')
        return v
```

## Database Migrations (Alembic)

### Create Migration
```bash
alembic revision --autogenerate -m "Add new field"
```

### Apply Migration
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

## Testing Routes

### Using TestClient
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_student():
    response = client.post("/api/v1/academic/admin/students", json=[
        {
            "student_id": "S001",
            "name": "John Doe",
            "dob": "2000-01-01",
            "academic_records": []
        }
    ])
    assert response.status_code == 200
```

## Environment Variables

### Required (.env file)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/verifiable_stubs
API_TITLE=Verifiable Stubs APIs
API_VERSION=1.0.0
LOG_LEVEL=INFO
APP_ENV=development
```

## Logging

### Setup in Routes
```python
import logging

logger = logging.getLogger(__name__)

@router.get('/items')
def get_items(db: Session = Depends(get_db)):
    logger.info("Fetching all items")
    items = db.query(MyModel).all()
    logger.debug(f"Found {len(items)} items")
    return items
```

## Tips & Tricks

1. **Automatic Validation**: Pydantic models validate all incoming data
2. **Automatic Docs**: Just add docstrings to routes for documentation
3. **Query Parameters**: Add as function parameters for automatic parsing
4. **Path Parameters**: Use `{param}` in path string and add as function parameter
5. **Headers**: Use `Header()` from FastAPI for header parameters
6. **Cookies**: Use `Cookie()` from FastAPI for cookie parameters
7. **Async Support**: Change `def` to `async def` and use `await` in routes
8. **Middleware**: Can be added via `app.add_middleware()`
9. **CORS**: Already configured in `app.core.app.py`
10. **Database Sessions**: Always use `Depends(get_db)` for type-safe sessions

## Troubleshooting

### Route Not Found
- Check router is registered in `app/core/app.py`
- Verify prefix matches URL path

### Validation Error
- Check Pydantic schema matches request body
- Review field types and constraints

### Database Error
- Ensure models inherit from `app.core.database.Base`
- Check DATABASE_URL environment variable
- Verify database is running

### Import Errors
- Check imports use new module paths
- Verify `__init__.py` files exist in all packages

---

**Last Updated:** December 18, 2025
