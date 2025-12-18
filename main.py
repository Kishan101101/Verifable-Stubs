"""Primary entrypoint exposing `app` for servers like `uvicorn` or `gunicorn`.

Usage examples:
- Development with uvicorn (ASGI adapter): `uvicorn main:app --host 0.0.0.0 --port 8000`
- Gunicorn (WSGI): `gunicorn --bind 0.0.0.0:8000 run:app` (or use a worker class)
"""
import os
from asgiref.wsgi import WsgiToAsgi
from app import create_app


# Create Flask WSGI app
flask_app = create_app(os.getenv("FLASK_ENV", "development"))

# Wrap as ASGI so servers like `uvicorn` can run it directly
asgi_app = WsgiToAsgi(flask_app)

# Expose `app` name for uvicorn: `uvicorn main:app`
app = asgi_app


if __name__ == "__main__":
    # fallback for running directly: start Flask development server
    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
