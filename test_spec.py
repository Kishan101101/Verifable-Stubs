from app import create_app
import json

app = create_app()
with app.test_client() as c:
    spec = json.loads(c.get('/openapi.json').data)
    print('Paths found:', len(spec['paths']))
    print('Endpoints:')
    for path in sorted(spec['paths'].keys()):
        print(f"  {path}")
