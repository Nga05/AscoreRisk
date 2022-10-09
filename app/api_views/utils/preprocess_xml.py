import numpy as np
import pandas as pd
from xml_parse_bs4 import xml_parse
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import glob

# get all xml files
folder_xml_path = str(Path(__file__).parent/ "xml")
files = [f for f in glob.glob(folder_xml_path + "/*.xml")]
print(files)

## Tets xml_parse main function
path_xml_file = str(Path(__file__).parent/ "xml/000186042261.xml")
xml_df = xml_parse(path_xml_file)

# convert to datetime 
xml_df['ngay_bat_dau'] = pd.to_datetime(xml_df['ngay_bat_dau'], format='%d%m%Y')
xml_df['ngay_ket_thuc'] = pd.to_datetime(xml_df['ngay_ket_thuc'], format='%d%m%Y')
xml_df['pcb_req_res_timestamp'] = pd.to_datetime(xml_df['pcb_req_res_timestamp'], format='%Y-%m-%d')
# calc diff dates
xml_df['thoi_han_vay'] = (xml_df['ngay_ket_thuc'] - xml_df['ngay_bat_dau'])/np.timedelta64(1, 'D')

# Create 'loai_khoan_vay' feature
xml_df[['loai_khoan_vay']] = ""
for i, val in enumerate(xml_df['loantype']):
    if val == 'Instalments':
        xml_df['loai_khoan_vay'][i] = 'Vay_Thong_Thuong'
    elif val == 'NonInstalments':
        xml_df['loai_khoan_vay'][i] = 'Vay_Thau_Chi'
    else:
        xml_df['loai_khoan_vay'][i] = 'The_Tin_Dung'

# create 'tenor_khoan_vay' feature based on 'thoi_han_vay' and 'giai_doan_hdv_map'
khong_co_khoan_vay = ['RQ', 'RN', 'RF']
co_khoan_vay = ['LV', 'TM', 'TA']
khoan_vay_hoan_tat = ['TM', 'TA']
xml_df[['tenor_khoan_vay']]= ""
for i, val in enumerate(xml_df['thoi_han_vay']):
    if (val <= 360) and (xml_df['giai_doan_hdv_map'][i] in co_khoan_vay):
        xml_df['tenor_khoan_vay'][i] = "ngan_han"
    elif (val <=1800) and (xml_df['giai_doan_hdv_map'][i] in co_khoan_vay):
        xml_df['tenor_khoan_vay'][i] = "trung_han"
    elif (val > 1800) and (xml_df['giai_doan_hdv_map'][i] in co_khoan_vay):
        xml_df['tenor_khoan_vay'][i] = 'dai_han'
    else:
        xml_df['tenor_khoan_vay'][i] = "khong_co_khoan_vay"
