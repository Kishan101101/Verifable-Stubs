"""Primary entrypoint exposing `app` for servers like `uvicorn` or `gunicorn`.

Usage examples:
- Development with uvicorn: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Gunicorn (with workers): `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000`
"""
import os
import logging
from contextlib import asynccontextmanager
from app.core.app import create_app

# Suppress Uvicorn banner on startup
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)

# Create FastAPI app
app = create_app(os.getenv("APP_ENV", "development"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_config=None)

