# coding: utf-8
import uuid
import json
import urllib.request
import datetime

# order
str_order = 'sample'

# Request setting
str_url = 'http://store/'
str_method = 'POST'
dict_headers = {
    'Content-Type': 'application/json'
}

# process something

# create order queue
str_id = str(uuid.uuid4())
dict_queue = {
    'order': str_order,
    'receipt': {
        'sample_datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'sample_id': str_id
    }
}

try:
    # Request order
    request = urllib.request.Request(
        str_url,
        data=json.dumps(dict_queue).encode('utf-8'),
        method=str_method,
        headers=dict_headers
    )
    with urllib.request.urlopen(request) as response:
        str_response = response.read().decode('utf-8')
        print('Response: ', str_response)
except Exception as e:
    print('Error: ', e)
