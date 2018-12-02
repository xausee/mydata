#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import random
from flask import Flask, request
from db import db

app = Flask(__name__)


# @app.route("/")
# def hello():
#     return "Hello World!"


@app.route("/getRandomPoem", methods=['POST'])
def get_random_poems():
    count = db.poem.find().count()
    cursor = db.poem.find().limit(1).skip(random.randint(1, count - 1))
    data = {}
    for doc in cursor:
        doc.pop("_id")
        data = doc
        break

    return json.dumps(data)


@app.route("/getPoem", methods=['POST'])
def get_poem():
    data = json.loads(request.get_data().decode())
    poem_id = data['id']
    # poem = db.poem.find_one({"_id": ObjectId(poem_id)})
    poem = db.poem.find_one({"id": poem_id})
    poem.pop("_id")
    return json.dumps(poem)


@app.route("/searchPoem", methods=['POST'])
def search_poem():
    data = json.loads(request.get_data().decode("utf8"))
    key = data['key']

    query = {"$or": [{'author': {'$regex': key}}, {'title': {'$regex': key}}, {'content': {'$regex': key}}]}

    if "author" in data:
        query = {'author': {'$regex': key}}

    poem_col = db.poem.find(query).limit(50)
    data = list()
    for doc in poem_col:
        doc.pop("_id")
        data.append(doc)
    return json.dumps(data)


@app.route("/getPoets", methods=['POST'])
def get_poets():
    data = json.loads(request.get_data().decode())

    query = {}

    if "genre" in data:
        query["genres"] = {"$in": [data["genre"]]}

    if "chronology" in data:
        query["chronology"] = data["chronology"]

    if "alphabetIndex" in data:
        query["alphabetindex"] = data["alphabetindex"]

    # 随机查询
    # if "amount" in data:
    #     poets_list = [
    #         {
    #             "id": poet["id"],
    #             "name": poet["name"]
    #         } for poet in
    #         db.poet.aggregate([{"$sample": {"size": data["amount"]}}])
    #     ]

    if "amount" in data:
        poets_list = [
            {
                "id": poet["id"],
                "name": poet["name"],
                "alphabetIndex": poet["alphabetindex"],
                "chronology": poet["chronology"],
                "genres": poet["genres"],
            } for poet in
            db.poet.find(query).limit(data["amount"])
        ]
    else:
        poets_list = [
            {
                "id": poet["id"],
                "name": poet["name"],
                "alphabetIndex": poet["alphabetindex"],
                "chronology": poet["chronology"],
                "genres": poet["genres"],
            } for poet in
            db.poet.find(query)
        ]

    return json.dumps(poets_list)


@app.route("/getPoetData", methods=['POST'])
def get_poet_data():
    data = json.loads(request.get_data().decode("utf8"))
    poet_id = data['poetId']

    data = dict()

    poet_document = db.poet.find({"id": poet_id}).limit(1)[0]

    poems = list()
    for doc in db.poem.find({"authorid": poet_id}):
        poems.append({"id": doc["id"], "title": doc["title"]})

    data["id"] = poet_document["id"]
    data["name"] = poet_document["name"]
    data["chronology"] = poet_document["chronology"]
    data["genres"] = poet_document["genres"]
    data["intro"] = poet_document["intro"]
    data["poems"] = poems

    return json.dumps(data)


@app.route("/getGenres", methods=['POST'])
def get_genres():
    data = json.loads(request.get_data().decode())

    query = {}

    if "name" in data:
        query["name"] = data["name"]

    if "chronology" in data:
        query["chronology"] = data["chronology"]

    if "alphabetIndex" in data:
        query["alphabetindex"] = data["alphabetindex"]

    genre_list = [
        {
            "id": genre["id"],
            "name": genre["name"],
            "alphabetIndex": genre["alphabetindex"],
            "chronology": genre["chronology"],
            "description": genre["description"],
        } for genre in
        db.genre.find(query)
    ]

    return json.dumps(genre_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=False, ssl_context=("cert/full_chain.pem", "cert/private.key"))
