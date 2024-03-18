from flask import Flask
import tabula
import pandas as pd
import warnings
from pypdf import PdfReader
import os
import pymongo
import numpy as np
from pdf_downloader import link_to_pdf_storage
from flask import request
from main import *
from flask import Response
from flask_cors import cross_origin
from flask import jsonify
warnings.simplefilter(action='ignore', category=FutureWarning)
app = Flask(__name__)

class FooException(Exception):
    """ Binds optional status code and encapsulates returing Response when error is caught """
    def __init__(self, *args, **kwargs):
        code = kwargs.pop('code', 400)
        Exception.__init__(self)
        self.code = code

    def as_http_error(self):
        return Response(str(self), self.code)

downloader_obj = link_to_pdf_storage()
to_mongo_db_obj = main_function()

@app.route('/')
@cross_origin()
def index():
    return 'index_page'

@app.route('/link_to_mongo_db', methods=["POST"])
@cross_origin()
def link_to_mongo_db():
    try:
        data = request.get_json()
        downloader_obj.Ten_K_report(data['Link'], data['Target'])
        to_mongo_db_obj.read_pdf_file_from_storage_to_mongodb()
        return f'Insert {data["Target"]} success from {data["Link"]}'
    except FooException as ex:
        return ex.as_http_error()

@app.route('/read_data_from_mongo_db', methods=["POST"])
@cross_origin()
def read_data_from_mongo_db():
    try:
        data = request.get_json()
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Company_financial_report"]
        col = db["10Q_report"]
        x = col.find_one({"Name": data['Target']},{"Name": 1,"Total current assets": 1, "Inventory": 1,"_id": 0,"Total current liabilities": 1,"Date":1, "Inventories": 1})
        print(x['Name'])
        if data['Target'] == 'nvidia':
            x['Inventory'] = x['Inventories']
        return jsonify(x)
    except FooException as ex:
        return ex.as_http_error()

@app.route('/read_chart_from_mongo_db', methods=["POST"])
@cross_origin()
def read_chart_from_mongo_db():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Company_financial_report"]
        col = db["Quarterly_presentation"]
        x = col.find_one({},{'Q4 FY23': 1,"Q1 FY24": 1, "Q2 FY24": 1,"_id": 0,"Q3 FY24": 1,"Q4 FY24":1})
        return jsonify(x)
    except FooException as ex:
        return ex.as_http_error()