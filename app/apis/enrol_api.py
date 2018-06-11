# coding=utf-8

from flask import Blueprint, request
from flask_restful import Api, Resource

from app.foundation import db
from app.service import EnrolInformationService

enrol_api_bp = Blueprint('EnrolApi', __name__)
enrol_api = Api(enrol_api_bp)


class EnrolInformation(Resource):

    def get(self):
        return {'hello': 'world'}

    def post(self):
        params = request.values.to_dict()
        print params
        EnrolInformationService(db).create(
            real_name=params.get('params'),
            id_number=params.get('id_number'),
            gender=params.get('gender'),
            phone=params.get('phone'))
        db.session.commit()
        return params, 200


enrol_api.add_resource(EnrolInformation, '/enrol-information')
