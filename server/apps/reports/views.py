"""
Views do módulo de relatórios	

"""
from flask import Blueprint, request
from marshmallow import Schema, fields
from .api import ReportApi
from server.apps.hardware.validators import validate_group

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/', methods=['GET'])
def list_reports():
	return ReportApi().list()


@bp.route('/', methods=['POST'])
def create_reports():

	class ReportRequest(Schema):
		group_id = fields.String(required=True, validate=validate_group)

	data = request.json
	try:
		ReportRequest().load(data)
		return ReportApi().create(data)
	
	except Exception as error:
		print(error)
		return str(error), 400
