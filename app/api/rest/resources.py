"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request, jsonify
from flask_restplus import Api
import os.path
import json

from app.api.rest.base import BaseResource, SecureResource
from app.api import api_rest


categories = ["dresses", "jackets", "tops", "jeans", "pants"]

def get_clothes_from_file(fname="all_products.json"):
    try:
        fname = os.path.join(os.path.dirname(__file__), fname)
        with open(fname, "r") as f:
            _data = json.load(f)
    except:
        _data = {cat: {} for cat in categories}
        print(f"something went wrong with reading {fname}")
    return dict(_data)


@api_rest.route("/products")
class Products(BaseResource):

    def get(self):
        # get all products or prod categories with ?cat=x
        data = get_clothes_from_file()
        # print(request.args)
        if "cat" in request.args:
            cat = request.args["cat"]
            data = data[cat] if cat in data else data
        return jsonify(data)

@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(BaseResource):
    """ Sample Resource Class """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {"timestamp": timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {"timestamp": json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

