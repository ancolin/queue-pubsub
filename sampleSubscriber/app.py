# coding: utf-8
import json
import urllib.request

# order
str_order = 'sample'
int_limit = 3

# Request setting
str_url = 'http://store/'
str_method = 'GET'

try:
    # Request order
    request = urllib.request.Request(
        str_url + '?order=' + str_order + '&limit=' + str(int_limit),
        method=str_method
    )
    with urllib.request.urlopen(request) as response:
        dict_response = json.loads(response.read().decode('utf-8'))
        if 'result' in dict_response and dict_response['result'] == 'OK':
            list_queues = dict_response['queues']
            for dict_queue in list_queues:
                # process something
                print('Queue: ', dict_queue)
        else:
            print('Error: ', dict_response)

except Exception as e:
    print('Error: ', e)
