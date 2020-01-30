# coding: utf-8
from flask import Flask, jsonify, request
import redis
import json
import datetime
import uuid

app = Flask(__name__)


@app.route('/', methods=['POST'])
def pushQueue():
    str_result = 'NG'
    int_status_code = 400
    str_message = ''
    dict_message = {}

    # check Content-Type
    if not request.headers.get("Content-Type") == "application/json":
        str_message = "not supported Content-Type."
    else:
        try:
            payload = request.json

            # check Request
            if 'order' not in payload or 'receipt' not in payload:
                str_message = 'Mandatory keys is missing.'
            else:
                try:
                    # push queue
                    string_id = str(uuid.uuid4())
                    dict_queue = {
                        'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                        'id': string_id,
                        'receipt': payload['receipt']
                    }
                    r = redis.Redis(host='redis', port=6379, db=0)
                    r.lpush(payload['order'], json.dumps(dict_queue))

                    str_result = 'OK'
                    dict_message = {
                        'order': payload['order'],
                        'id': string_id
                    }
                    int_status_code = 200
                except Exception as e:
                    int_status_code = 500
                    str_message = 'Internal server error.'
                    print('Error: ', e)

        except Exception as e:
            str_message = 'Bad request.'
            print('Error: ', e)

    # response
    if str_result == "OK":
        dict_response = {"result": str_result, 'queue': dict_message}
    else:
        dict_response = {"result": str_result, "errors": str_message}
    return jsonify(dict_response), int_status_code


@app.route('/', methods=['GET'])
def popQueue():
    str_result = 'NG'
    int_status_code = 400
    str_message = ''

    try:
        dict_params = request.args

        # check Request
        if 'order' not in dict_params:
            str_message = 'Mandatory keys is missing.'
        else:
            try:
                int_limit = 1
                if 'limit' in dict_params:
                    try:
                        int_limit = int(dict_params['limit'])
                    except Exception as e:
                        int_limit = 0
                        str_message = 'Invalid data type: limit'
                        print('Error: ', e)

                # pop queue
                if int_limit > 0:
                    list_queues = []
                    while int_limit > 0:
                        r = redis.Redis(host='redis', port=6379, db=0)
                        str_queue = r.rpop(dict_params['order'])
                        if str_queue is not None:
                            list_queues.append(json.loads(str_queue))
                            int_limit -= 1
                        else:
                            int_limit = 0

                    str_message = list_queues
                    str_result = 'OK'
                    int_status_code = 200
            except Exception as e:
                int_status_code = 500
                str_message = 'Internal server error.'
                print('Error: ', e)

    except Exception as e:
        str_message = 'Bad request.'
        print('Error: ', e)

    # response
    if str_result == "OK":
        response = {"result": str_result, 'queues': str_message}
    else:
        response = {"result": str_result, "errors": str_message}
    return jsonify(response), int_status_code


if __name__ == '__main__':
    app.run()
