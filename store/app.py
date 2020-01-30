# coding: utf-8
from flask import Flask, jsonify, request, abort
import redis
import json
import datetime
import uuid

app = Flask(__name__)


@app.route('/', methods=['POST'])
def pushQueue():
    result = "NG"
    status_code = 400

    # check Content-Type
    if not request.headers.get("Content-Type") == "application/json":
        message = "not supported Content-Type."
    else:
        try:
            payload = request.json

            # check Request
            if 'order' not in payload or 'receipt' not in payload:
                message = 'Mandatory keys is missing.'
            else:
                try:
                    # push queue
                    string_id = str(uuid.uuid4())
                    queue = {
                        'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                        'id': string_id,
                        'receipt': payload['receipt']
                    }
                    r = redis.Redis(host='redis', port=6379, db=0)
                    r.lpush(payload['order'], json.dumps(queue))

                    result = 'OK'
                    message = {
                        'order': payload['order'],
                        'id': string_id
                    }
                    status_code = 200
                except Exception as e:
                    status_code = 500
                    message = 'Internal server error.'
                    print('Error: ', e)

        except Exception as e:
            message = 'Bad request.'
            print('Error: ', e)

    # response
    if result == "OK":
        response = {"result": result, 'queue': message}
    else:
        response = {"result": result, "errors": message}
    return jsonify(response), status_code


@app.route('/', methods=['GET'])
def popQueue():
    result = 'NG'
    status_code = 400

    try:
        params = request.args

        # check Request
        if 'order' not in params:
            message = 'Mandatory keys is missing.'
        else:
            try:
                integer_limit = 1
                if 'limit' in params:
                    try:
                        integer_limit = int(params['limit'])
                    except Exception as e:
                        integer_limit = 0
                        message = 'Invalid data type: limit'
                        print('Error: ', e)

                # pop queue
                if integer_limit > 0:
                    queues = []
                    while integer_limit > 0:
                        r = redis.Redis(host='redis', port=6379, db=0)
                        queue = r.rpop(params['order'])
                        if queue is not None:
                            queues.append(json.loads(queue))
                            integer_limit -= 1
                        else:
                            integer_limit = 0

                    message = queues
                    result = 'OK'
                    status_code = 200
            except Exception as e:
                status_code = 500
                message = 'Internal server error.'
                print('Error: ', e)

    except Exception as e:
        message = 'Bad request.'
        print('Error: ', e)

    # response
    if result == "OK":
        response = {"result": result, 'queues': message}
    else:
        response = {"result": result, "errors": message}
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run()
