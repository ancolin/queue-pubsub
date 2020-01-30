# coding: utf-8
import uuid
import json
import urllib.request
import datetime

sample_id = str(uuid.uuid4())
queue = {
    'order': 'sample',
    'receipt': {
        'sample_datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'sample_id': sample_id
    }
}

url = 'http://store/'
method = 'POST'
headers = {
    'Content-Type': 'application/json'
}

try:
    request = urllib.request.Request(
        url,
        data=json.dumps(queue).encode('utf-8'),
        method=method,
        headers=headers
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        print('Response: ', response_body)
except Exception as e:
    print('Error: ', e)
