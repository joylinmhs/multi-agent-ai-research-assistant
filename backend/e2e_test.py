import requests
from pathlib import Path
p = Path('tmp_upload_test.txt')
p.write_text('Document A: apples are red and tasty')
with p.open('rb') as f:
    files = {'file': ('tmp_upload_test.txt', f, 'text/plain')}
    r = requests.post('http://127.0.0.1:8000/api/v1/documents/upload', files=files)
    print('UPLOAD', r.status_code)
    print(r.text)
    if r.ok:
        q = requests.post('http://127.0.0.1:8000/api/v1/chat/query', json={'query': 'What color are apples?', 'session_id': 'test'})
        print('CHAT', q.status_code)
        print(q.text)
