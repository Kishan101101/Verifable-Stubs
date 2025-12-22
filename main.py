"""Primary entrypoint exposing `app` for servers like `uvicorn` or `gunicorn`.

Usage examples:
- Development with uvicorn: `uvicorn main:app --host 0.0.0.0 --port 8001`
- Gunicorn (with workers): `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001`
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
    port = int(os.getenv("PORT", 8001))
    os.environ["PORT"] = str(port)  # Set for lifespan logging
    uvicorn.run(app, host="0.0.0.0", port=port, log_config=None)

