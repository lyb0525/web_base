# coding=utf-8
from flask import Blueprint, jsonify

frontend_api = Blueprint('frontend_api', __name__, template_folder='templates')

@frontend_api.route("/")
def api():
    data = {
      'foo': 'bar',
    }
    response = jsonify(data)
    response.status_code = 200
    return response
