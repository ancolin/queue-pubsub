# coding: utf-8
import uuid
import json
import urllib.request
import datetime

# order
order = 'sample'

# Request setting
url = 'http://store/'
method = 'GET'

try:
    # Request order
    request = urllib.request.Request(
        url + '?order=' + order,
        method=method
    )
    with urllib.request.urlopen(request) as response:
        response_json = json.loads(response.read().decode('utf-8'))
        if 'queue' in response_json and type(response_json['queue']) == dict:
            # process something
            print('Queue: ', response_json['queue'])
        elif 'queue' in response_json and type(response_json['queue']) == str:
            # process something
            print('Queue: ', response_json['queue'])
        else:
            # process something
            print('Queue: ', response_json['queue'])

except Exception as e:
    print('Error: ', e)
