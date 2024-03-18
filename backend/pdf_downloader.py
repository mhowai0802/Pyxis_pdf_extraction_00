import requests
import os

class link_to_pdf_storage():

    def Ten_K_report(self, url, target):
        number_of_files = 0
        for file in os.listdir("./Storage"):
            if target in file:
                number_of_files += 1
        r = requests.get(url, stream=True)
        with open(f'./Storage/{target}_10Q_2023_0{number_of_files}.pdf', 'wb') as fd:
            for chunk in r.iter_content(2000):
                fd.write(chunk)
