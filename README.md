# Verifiable Stubs APIs

## Prerequisites

- **Docker** (for PostgreSQL)
- **Python 3.10+** (3.11 recommended)
- **Git**

---

## Quick Setup (Windows)

### Step 1: Clone Repository
```powershell
git clone <repo-url>
cd Verifable-Stubs
```

### Step 2: Setup Environment Variables
```powershell
copy .env.example .env
```
This creates your `.env` file with default values. Edit `.env` if needed (usually not required for local setup).

### Step 3: Start Database (Docker)
```powershell
docker ps
```
Should show `verifiable_stubs_db` running.

### Step 4: Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 5: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 6: Create Database Tables
```powershell
venv\Scripts\python -m alembic upgrade head
```


### Step 7: Start Server
```powershell
venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**→ Server is now running!**

---

## Quick Setup (macOS / Linux)

Same steps as Windows, but use:
```bash
cp .env.example .env
source venv/bin/activate
pip install -r requirements.txt
venv/bin/python -m alembic upgrade head
venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Swagger UI — Complete API Documentation

**Open your browser and go to:**
### **http://127.0.0.1:8000/swagger**

This is where you can:
- ✅ See all 25+ API endpoints
- ✅ View request/response schemas with all fields and types
- ✅ Test endpoints directly from the browser
- ✅ View response examples

---
