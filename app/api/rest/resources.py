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

def get_data_from_file(fname="all_products.json"):
    try:
        fname = os.path.join(os.path.dirname(__file__), fname)
        with open(fname, "r") as f:
            _data = json.load(f)
    except:
        _data = {cat: {} for cat in categories}
        print(f"something went wrong with reading {fname}")
    return dict(_data)

def search_data(term, cat=False):
    data = get_data_from_file()
    _data = []
    if not cat:
        for cat in data:
            for prod in data[cat]:
                for field in [prod["id"], prod["title"], prod["color"], prod["type"]]:
                    if term in field and prod not in _data:
                        _data.append(prod)
    else:
        for prod in data[cat]:
            for field in [prod["id"], prod["title"], prod["color"], prod["type"]]:
                    if term in field and prod not in _data:
                        _data.append(prod)
    return _data

def chunk_data(data, size):
    _chunked = [data[i:i+size] for i in range(0,len(data),size)]
    if len(_chunked) > 15:
        size *= 2
        _chunked = [data[i:i+size] for i in range(0,len(data),size)]
    return _chunked

def sort_colors(data, cols):
    _data = []
    if type(cols) is str:
        cols = [cols]
    for col in cols:
        for prod in data:
            if col == prod['color']:
                _data.append(prod)
    return _data

@api_rest.route("/products")
class Products(BaseResource):

    def get(self):
        chunksize = 30
        data = get_data_from_file()
        args = request.args
        # category og search term
        if 'cat' in args and 'term' in args:
            data = search_data(args['term'], args['cat'])
        elif 'cat' in args:
            data = data[args['cat']]
        elif 'term' in args:
            data = search_data(args['term'])
        else:
            data = data['dresses']

        # sorting
        if 'sort' in args:
            if args['sort'] == 'hilo':
                data = sorted(data, key=lambda x: float(x['price']), reverse=True)
            else:
                data = sorted(data, key=lambda x: float(x['price']))

        # colors
        if 'cols' in args:
            cols = args['cols']
            print(cols)
            if ',' in cols:
                cols = cols.split(',')
                data = sort_colors(data, cols)
            else:
                data = sort_colors(data, cols)

        return jsonify(chunk_data(data, chunksize))

@api_rest.route("/products/<string:pid>")
class Products(BaseResource):

    def get(self, pid):
        data = get_data_from_file()
        for cat in data:
            for prod in data[cat]:
                if pid == prod['id']:
                    return jsonify(prod)
        raise Exception("not found")

@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
