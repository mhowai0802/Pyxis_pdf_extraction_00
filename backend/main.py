import tabula
import pandas as pd
import warnings
from pypdf import PdfReader
import os
import pymongo
import numpy as np
from pdf_downloader import link_to_pdf_storage
warnings.simplefilter(action='ignore', category=FutureWarning)

class main_function():

    def read_pdf_output_balance_sheet_as_dataframe(self,path):
        reader = PdfReader(path)
        dict = {}
        for index, page in enumerate(reader.pages):
            text = page.extract_text().lower()
            if index == 1:
                splited_text = text.split(" ")
                if len(splited_text) == 1:
                    splited_text = splited_text[0].split('\t')
                dict["Name"] = splited_text[0].strip(",")
                for index, element in enumerate(splited_text):
                    if 'ended' in element:
                        date = splited_text[index + 1] + splited_text[index + 2] + splited_text[index + 3]
                        dict["Date"] = date.strip('table').strip('\n').strip('\nindex')
                        break
            if 'balance' in text and 'index' not in text and 'sheet' in text and 'goodwill' in text:
                dfs = tabula.read_pdf(path, pages=f'{index + 1}')[0]
                dfs = dfs.fillna('null')
                for index, row in dfs.iterrows():
                    money = 1
                    while row[money] == 'null' or row[money] == '$':
                        money += 1
                        if abs(money) == len(row) - 1:
                            break
                    dict[row[0]] = row[money]
                return dict

    def read_pdf_file_from_storage_to_mongodb(self):
        master = []
        for file in os.listdir("./Storage"):
            pdf_directory = f"./Storage/{file}"
            master.append(self.read_pdf_output_balance_sheet_as_dataframe(pdf_directory))
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Company_financial_report"]
        mycol = mydb["10Q_report"]
        for mydict in master:
            mycol.insert_one(mydict)