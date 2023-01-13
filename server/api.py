import json
from bson import json_util 
from flask import jsonify
from server.driver import db

class BaseApi():
	base_methods = ["list", "retrieve", "create"]

	def list(self):
		data = db()[self.collection].find({})
		data = json.loads(json_util.dumps(data)) 
		return jsonify(list(data))
	
	def retrieve(self, id):
		data = db()[self.collection].find({"id": id})
		data = json.loads(json_util.dumps(data)) 
		return jsonify(dict(data))
	
	def create(self, data):
		try:
			self.model.load(data)
		except Exception as error:
			return str(error), 400		

		data = self.model.dump(data)
		db()[self.collection].insert_one(data)
		return jsonify(dict(data))
    