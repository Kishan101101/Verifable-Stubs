from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .logging_config import configure_logging

db = SQLAlchemy()


def create_app(config_name='development'):
    """Application factory"""
    from config import config

    # configure logging early so extension init and imports are logged
    configure_logging()

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Create tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from app.routes.doctor_onboarding import doctor_bp
    from app.routes.academic_admission import academic_bp
    from app.routes.insurance_claim import insurance_bp

    app.register_blueprint(doctor_bp, url_prefix='/api/v1/doctors')
    app.register_blueprint(academic_bp, url_prefix='/api/v1/academic')
    app.register_blueprint(insurance_bp, url_prefix='/api/v1/insurance')

    # Health check route
    @app.route('/api/v1/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Verifiable Stubs API is running'}, 200

    # Favicon endpoint (suppress 404)
    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        """Return a minimal favicon to suppress 404 errors."""
        return '', 204

    # OpenAPI spec endpoint
    @app.route('/openapi.json', methods=['GET'])
    def openapi_spec():
        """Return OpenAPI 3.0 spec with proper Pydantic schemas."""
        from app.openapi_generator import pydantic_to_openapi_schema, get_schema_class, ROUTE_SCHEMAS
        
        paths = {}
        
        # Iterate all routes in the app
        for rule in app.url_map.iter_rules():
            # Skip internal routes
            if rule.endpoint in ['openapi_spec', 'swagger_ui', 'favicon', 'static']:
                continue
            
            path = rule.rule
            methods = [m.lower() for m in rule.methods if m not in ['HEAD', 'OPTIONS']]
            
            if not methods:
                continue
            
            if path not in paths:
                paths[path] = {}
            
            for method in methods:
                view_func = app.view_functions.get(rule.endpoint)
                docstring = (view_func.__doc__ or '').strip() if view_func else ''
                summary = docstring.split('\n')[0] if docstring else f'{method.upper()} {path}'
                
                # Extract tag from path
                path_parts = path.split('/')
                tag = path_parts[3] if len(path_parts) > 3 else 'API'
                
                operation = {
                    'summary': summary,
                    'tags': [tag],
                    'responses': {
                        '200': {
                            'description': 'Successful response',
                            'content': {
                                'application/json': {
                                    'schema': {'type': 'object'}
                                }
                            },
                        },
                        '400': {'description': 'Bad request'},
                        '500': {'description': 'Server error'},
                    },
                }
                
                # Load schema mapping if available
                route_schema_map = ROUTE_SCHEMAS.get(path, {})
                
                # Add request body for POST/PUT/PATCH with proper schema
                if method in ['post', 'put', 'patch']:
                    request_schema_name = route_schema_map.get('request')
                    request_schema_class = get_schema_class(request_schema_name) if request_schema_name else None
                    
                    if request_schema_class:
                        request_schema = pydantic_to_openapi_schema(request_schema_class)
                    else:
                        request_schema = {'type': 'object'}
                    
                    operation['requestBody'] = {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': request_schema
                            }
                        },
                    }
                
                # Add response schema if mapped
                response_schema_name = route_schema_map.get('response')
                if response_schema_name:
                    response_schema_class = get_schema_class(response_schema_name)
                    if response_schema_class:
                        response_schema = pydantic_to_openapi_schema(response_schema_class)
                        operation['responses']['200']['content']['application/json']['schema'] = response_schema
                
                # Add path parameters for GET
                if method == 'get' and '{' in path:
                    operation['parameters'] = [
                        {
                            'name': param.strip('{}'),
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                        }
                        for param in path.split('/')
                        if '{' in param
                    ]
                
                paths[path][method] = operation
        
        return jsonify({
            'openapi': '3.0.0',
            'info': {
                'title': app.config.get('API_TITLE', 'Verifiable Stubs APIs'),
                'version': app.config.get('API_VERSION', '1.0.0'),
                'description': 'Flask APIs for doctor onboarding, academic admission, and insurance claim flows.',
            },
            'paths': paths,
            'servers': [
                {'url': 'http://127.0.0.1:8000', 'description': 'Local development'},
                {'url': 'http://0.0.0.0:8000', 'description': 'Local network'},
            ],
        })

    # Swagger UI endpoint
    @app.route('/swagger', methods=['GET'])
    def swagger_ui():
        """Serve Swagger UI from CDN."""
        html = '''<!DOCTYPE html>
<html>
  <head>
    <title>Swagger UI - Verifiable Stubs APIs</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
    <style>
      html {
        box-sizing: border-box;
        overflow: -moz-scrollbars-vertical;
        overflow-y: scroll;
      }
      *, *:before, *:after {
        box-sizing: inherit;
      }
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "BaseLayout"
      })
    }
    </script>
  </body>
</html>
'''
        return html

    return app
