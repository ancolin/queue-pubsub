# coding: utf-8
from flask import Flask, jsonify, request, abort
import redis
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def orderQueue():
    result = "NG"
    message = ""
    if not request.headers.get("Content-Type") == "application/json":
        message = "not supported Content-Type."
    else:
        try:
            r = redis.Redis(host='redis', port=6379, db=0)
            r.lpush('orderQueue', json.dumps(request.json))
            result = "OK"
        except Exception as e:
            message = e

    if result == "OK":
        response = {"result": result}
    else:
        response = {"result": result, "errors": message}

    return jsonify(ResultSet=response)


if __name__ == '__main__':
    app.run()
