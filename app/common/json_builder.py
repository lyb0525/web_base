# coding=utf-8

import json
from datetime import date, datetime
from flask import jsonify


def success_result(data={}, page={}):
    ret = {
        'code': 0,
        'data': data,
        'page': page
    }
    return jsonify(ret)

def error_requests(status_code=440, data={}):
    response = jsonify(data)
    response.status_code = status_code
    return response

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
