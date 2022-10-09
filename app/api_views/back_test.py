import logging
from ascore_fastapi import Backtest
from pathlib import Path
import glob
import pandas as pd
import csv
import time

class CSVData:
    def __init__(self, data: dict, path):
        self.data = data
        self.path = path
    def build(self, filename, datamodel):
        self.data['Filename'] = filename
        self.data['Ascore_respone'] = datamodel
    def save(self):
        df = pd.DataFrame(self.data, columns=[self.data.keys[0], self.data.keys[1]])
        df.to_csv(self.path)
    

if __name__ == "__main__":
    # XmlFolder = str(Path(__file__).parent / "utils/xml/1_patch")
    # xml_files = [f for f in glob.glob(XmlFolder + "/*.xml")]
    path_rs = str(Path(__file__).parent / "utils/xml/log_result/ascore_model_test_3.csv")
    xml_files = [str(Path(__file__).parent / "utils/xml/1_patch/FICO_APPL00939435.xml")]
    dbfilepath = str(Path(__file__).parent / "utils/xml/f1_data/f1_ascore_input.csv")
    rs = {}
    data_all = []
    i=0
    str_time = time.time()
    for file in xml_files:
        rs = {}
        rs['Filename'] = file
        try:
            data = Backtest(file, dbfilepath).save_drool()
            rs['Ascore_respone'] = str(data)
            data_all.append(rs)
            i+=1
        except Exception as e:
            rs['Ascore_respone'] = ""
            logging.getLogger("Parse xml error at file: %s - with error info: %s " %(str(file), str(e)))
            data_all = data_all.append(rs)
            raise e
            # continue
        print("count: ", i)
        df = pd.DataFrame.from_dict(data_all, orient='columns')
        print(df)
        df.to_csv(path_rs, index=False)
    end_time = time.time()
    time_process = (end_time-str_time)/180
    print("Total of process time: %.2f (h)" %time_process)