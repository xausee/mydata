#!/usr/bin/python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
from utils import load_json
import logger as logger


class MongoConfig():
    def __init__(self, host=None, port=None, user_name=None, password=None, db_name=None):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name


def get_mongo_config():
    mongo_dic = load_json('db.json')
    config = MongoConfig()
    config.__dict__ = mongo_dic
    return config


config = get_mongo_config()
logger.suc("数据库地址：{0} 端口：{1}".format(config.host, config.port))

mongo_client = MongoClient(config.host, config.port)
mongo_client.CaoMang.authenticate(config.user_name, config.password)

db = mongo_client[config.db_name]
