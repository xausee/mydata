#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from db import db

app = Flask(__name__)


@app.route("/getRandomPoems", methods=['POST'])
def get_random_poems():
    poem_col = db.poem.find().limit(5)
    data = list()
    for doc in poem_col:
        doc.pop("_id")
        data.append(doc)
    return json.dumps(data)


@app.route("/getPoem", methods=['POST'])
def get_poem():
    id = request.form['id']
    poem = db.poem.find_one({"id": id})
    poem.pop("_id")
    return json.dumps(poem)


@app.route("/searchPoem", methods=['POST'])
def search_poem():
    data = json.loads(request.get_data().decode())
    key = data['key']
    qurey = {"$or": [{'author': {'$regex': key}}, {'title': {'$regex': key}}, {'content': {'$regex': key}}]}
    poem_col = db.poem.find(qurey).limit(5)
    data = list()
    for doc in poem_col:
        doc.pop("_id")
        data.append(doc)
    return json.dumps(data)
