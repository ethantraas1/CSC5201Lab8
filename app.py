from flask import Flask, request, jsonify
from service import ItemService
from models import Schema

import json

app = Flask(__name__)

@app.after_request
def add_headers(response):
   response.headers['Access-Control-Allow-Origin'] = "*"
   response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
   response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
   return response

@app.route("/")
def hello():
   return "Hello World!"

@app.route("/<name>")
def hello_name(name):
   return "Hello " + name

@app.route("/items", methods=["GET"])
def list_todo():
   return jsonify(ItemService().list())

@app.route("/items", methods=["POST"])
def create_todo():
   return jsonify(ItemService().create(request.get_json()))

@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
   return jsonify(ItemService().update(item_id, request.get_json()))

@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
   return jsonify(ItemService().get_by_id(item_id))

@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
   return jsonify(ItemService().delete(item_id))

if __name__ == "__main__":
   Schema()
