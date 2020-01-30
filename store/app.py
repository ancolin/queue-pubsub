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
    if not request.headers.get("Content-Type") == "application/json":
        message = "not supported Content-Type."
    else:
        try:
            payload = request.json
            string_order = ''
            dict_receipt = {}

            try:
                string_order = payload['order']
                dict_receipt = payload['receipt']
            except Exception as e:
                message = 'Mandatory keys is missing.'
                print(e)

            try:
                # add pushed datetime and uuid
                string_pushed_datetime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

                queue = {'datetime': string_pushed_datetime, 'uuid': str(uuid.uuid4()), 'receipt': dict_receipt}

                # push queue
                r = redis.Redis(host='redis', port=6379, db=0)
                r.lpush(string_order, json.dumps(queue))
                result = "OK"
            except Exception as e:
                message = 'Internal server error.'
                print(e)

        except Exception as e:
            message = 'Bad request.'
            print(e)

    if result == "OK":
        response = {"result": result}
    else:
        response = {"result": result, "errors": message}

    return jsonify(response)


if __name__ == '__main__':
    app.run()
