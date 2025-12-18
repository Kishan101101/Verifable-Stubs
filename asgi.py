from asgiref.wsgi import WsgiToAsgi
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))
# Wrap Flask WSGI app as ASGI
asgi_app = WsgiToAsgi(app)

# Expose `app` for uvicorn to pick up (module: app variable)
# Uvicorn command: `uvicorn asgi:asgi_app --host 0.0.0.0 --port 8000`
