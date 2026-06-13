import requests
with open('tmp_upload_test.txt','rb') as f:
    files={'file':('tmp_upload_test.txt', f, 'text/plain')}
    r = requests.post('http://127.0.0.1:8000/api/v1/documents/upload', files=files)
    print(r.status_code)
    print(r.text)
