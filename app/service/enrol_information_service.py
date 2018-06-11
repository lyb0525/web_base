#!coding: utf-8

from .base_service import BaseBareModelService

from app.models import EnrolInformation


class EnrolInformationService(BaseBareModelService):

    model = EnrolInformation
