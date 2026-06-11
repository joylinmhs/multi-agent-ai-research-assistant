import json
import time
from urllib.request import Request, urlopen

BASE = 'http://127.0.0.1:8000/api/v1'

headers = {'Content-Type': 'application/json'}

def post(path, payload):
    data = json.dumps(payload).encode('utf-8')
    req = Request(BASE + path, data=data, headers=headers, method='POST')
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

if __name__ == '__main__':
    print('Ingesting sample document...')
    ingest_payload = {'content': 'This is a sample document ingested for testing. It mentions Chroma and retrieval.', 'title': 'Sample Doc'}
    r = post('/documents/ingest', ingest_payload)
    print('Ingest response:', json.dumps(r, indent=2))

    # brief pause to ensure embedding pipeline completes
    time.sleep(1)

    print('\nQuerying research chat...')
    chat_payload = {'query': 'What does the sample document mention?', 'session_id': 'sample-session'}
    r2 = post('/chat/query', chat_payload)
    print('Chat response:', json.dumps(r2, indent=2))
