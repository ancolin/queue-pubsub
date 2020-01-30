# coding: utf-8
from flask import Flask, jsonify, request, abort
import redis
import json
import datetime
import uuid

app = Flask(__name__)


@app.route('/', methods=['POST'])
def orderQueue():
    result = "NG"
    message = ""

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
                except Exception as e:
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
    return jsonify(response)


if __name__ == '__main__':
    app.run()
