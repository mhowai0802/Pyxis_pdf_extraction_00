import os
import io
from PIL import Image
import pytesseract
import gc
import fitz
import pymongo

pdf_path = 'Presentation/NVDA-F4Q24-Quarterly-Presentation-FINAL.pdf'

dict = {}
dict['Company'] = 'NVDA'
dict['Analysis'] = 'NVDA-F4Q24-Quarterly-Presentation-FINAL Financial Summary'
doc = fitz.open(pdf_path) # open a document
for index,page in enumerate(doc):
    text = page.get_text()
    if "Financial Summary" in text:
        split_text = text.split("\n")
        print(split_text)
        for split_index,element in enumerate(split_text):
            if 'Q4 FY23' in element:
                for number in range(5):
                    dict[split_text[split_index+number]] = split_text[split_index + number -17]
                break
        break

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Company_financial_report"]
mycol = mydb["Quarterly_presentation"]
mycol.insert_one(dict)
