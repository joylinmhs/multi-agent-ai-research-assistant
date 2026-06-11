import json
from time import sleep
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('Posting ingest...')
resp = client.post('/api/v1/documents/ingest', json={
    'content': 'This is a sample document ingested through TestClient. It mentions Chroma and retrieval features.',
    'title': 'TestClient Doc'
})
print('Status:', resp.status_code)
try:
    print(json.dumps(resp.json(), indent=2))
except Exception:
    print(resp.text)

# small sleep to allow background tasks if any
sleep(0.5)

print('\nPosting chat query...')
resp2 = client.post('/api/v1/chat/query', json={
    'query': 'What topics does the test document mention?',
    'session_id': 'testclient'
})
print('Status:', resp2.status_code)
try:
    print(json.dumps(resp2.json(), indent=2))
except Exception:
    print(resp2.text)
