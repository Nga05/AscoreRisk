from bs4 import BeautifulSoup
from pathlib import Path
import numpy as np
import pandas as pd
from collections import defaultdict
import glob
import logging

def parse_contract_tag(tagname, bs):
    # from collections import defaultdict
    contract_data = {}
    contract_all = bs.find_all(tagname)
    CBContractCode, EncryptedFICode, ContractPhase, StartingDate, EndDateOfContract, TotalAmount, RequestDateOfTheContract = [],[],[],[],[],[], []
    if tagname == 'GrantedContract':
        for granted in contract_all:
            # get from "CommonData" tag
            commonData = granted.find('CommonData')
            CBContractCode.append(commonData.find('CBContractCode').text)
            EncryptedFICode.append(commonData.find('EncryptedFICode').text)
            ContractPhase.append(commonData.find('ContractPhase').text)
            StartingDate.append(commonData.find('StartingDate').text)
            EndDateOfContract.append(granted.find('EndDateOfContract').text)
            TotalAmount.append(granted.find('TotalAmount').text)
        contract_data['ma_hdv_tai_pcb']=CBContractCode
        contract_data['ma_tctd']=EncryptedFICode
        contract_data['giai_doan_hdv']=ContractPhase
        contract_data['ngay_bat_dau']=StartingDate
        contract_data['ngay_ket_thuc']=EndDateOfContract
        contract_data['so_tien_vay']=TotalAmount
    if tagname == 'NotGrantedContract':
        for notgranted in contract_all:
            CBContractCode.append(notgranted.find('CBContractCode').text)
            EncryptedFICode.append(notgranted.find('EncryptedFICode').text)
            ContractPhase.append(notgranted.find('ContractPhase').text)
            # get from "Amounts" tag
            Amount_tag = notgranted.find('Amounts')
            RequestDateOfTheContract.append(Amount_tag.find('RequestDateOfTheContract').text)
            EndDateOfContract.append('')
            TotalAmount.append(Amount_tag.find('TotalAmount').text)
        contract_data['ma_hdv_tai_pcb']=CBContractCode
        contract_data['ma_tctd']=EncryptedFICode
        contract_data['giai_doan_hdv']=ContractPhase
        contract_data['ngay_bat_dau']=RequestDateOfTheContract
        contract_data['ngay_ket_thuc']=EndDateOfContract
        contract_data['so_tien_vay']=TotalAmount
    return contract_data

def get_all_tagname(path_xml_file, tag_original):
    import xml.dom.minidom as md
    from itertools import chain
    parser_xml = md.parse(path_xml_file)
    tag_lst = []
    tag_of_tag_original = [[x.tagName for x in elem.childNodes] for elem in parser_xml.getElementsByTagName(tag_original)]
    tag_of_tag_original = list(chain.from_iterable(tag_of_tag_original)) # 2d -> 1d
    if len(tag_of_tag_original) > 0:
        for x in tag_of_tag_original:
            tag_lst.append(x)
    return tag_lst
    
def convert_to_table(dict_dt):
    import pandas as pd
    df = pd.DataFrame.from_dict(dict_dt, orient = 'columns')
    return df

def xml_parse(path_xml_file):  # replace path_xml_file to xml data from PCB database
    content = {
        "pcb_req_res_timestamp": "",
        "ma_khv_tai_pcb": '',
        "id_no": '',
        "diem": '',
        "loantype":
        {
            "Instalments": {
                "GrantedContract": {},
                "NotGrantedContract": {}
            },
            "NonInstalments": {
                "GrantedContract": {},
                "NotGrantedContract": {}
            },
            "Cards": {
                "GrantedContract": {},
                "NotGrantedContract": {}
            }
        }
    }
    file = open(path_xml_file, 'r')
    xml_content = file.read()
    bs = BeautifulSoup(xml_content, 'xml')
    try:
        content['pcb_req_res_timestamp'] = bs.find('MessageResponse').get_attribute_list('MTs')[0][:10]  # get only date
    except Exception:
        content['pcb_req_res_timestamp'] = ""
    try:
        content['ma_khv_tai_pcb'] = bs.find('CBSubjectCode').text
    except Exception:
        content['ma_khv_tai_pcb'] = ""
    try:
        content['id_no'] = bs.find('IDCard').text
    except Exception:
        content['id_no'] = ""
    try:
        content['diem'] = bs.find('ScoreRaw').text
    except Exception:
        content['diem'] = ""

    # extract loantype partition from xml data
    loantype = {}
    contract_tags = get_all_tagname(path_xml_file, 'Contract')
    for tag in contract_tags:
        if tag in ['Instalments', 'NonInstalments', 'Cards']:
            sub_tags = get_all_tagname(path_xml_file, tag)
            granted_data_all = {}
            granted_content = {} # defaultdict(list)
            not_granted_content = {}
            if 'GrantedContract' in sub_tags:
                granted_content = parse_contract_tag('GrantedContract', bs)
            if 'NotGrantedContract' in sub_tags:
                not_granted_content = parse_contract_tag('NotGrantedContract', bs)
            granted_data_all['GrantedContract'] = granted_content
            granted_data_all['NotGrantedContract'] = not_granted_content
            loantype[tag] = granted_data_all
    content['loantype'] = loantype
    ### convert xml content to dataframe
    df_all = pd.DataFrame()
    for ctr_type, ctr_val in content['loantype'].items(): # ctr_type = Instalments, NonInstalments, Cards
        # print(ctr_type)
        df_new = pd.DataFrame()
        for k, val in ctr_val.items():
            if bool(val): # val not empty
                df_sub = convert_to_table(val)
                df_sub['pcb_req_res_timestamp'] = content['pcb_req_res_timestamp']
                df_sub['ma_khv_tai_pcb'] = content['ma_khv_tai_pcb']
                df_sub['id_no'] = content['id_no']
                df_sub['diem'] = content['diem']
                df_sub['Sub_Contract'] = k
                df_sub['loantype'] = ctr_type
            else:
                print(ctr_type)
                continue
            df_new = pd.concat([df_new, df_sub])
        df_all = pd.concat([df_all, df_new])    
        return df_all

# def preprocess_xml(xml_df):
#     # convert to datetime 
#     xml_df['ngay_bat_dau'] = pd.to_datetime(xml_df['ngay_bat_dau'], format='%d%m%Y')
#     xml_df['ngay_ket_thuc'] = pd.to_datetime(xml_df['ngay_ket_thuc'], format='%d%m%Y')
#     xml_df['pcb_req_res_timestamp'] = pd.to_datetime(xml_df['pcb_req_res_timestamp'], format='%Y-%m-%d')
#     # calc diff dates
#     xml_df['thoi_han_vay'] = (xml_df['ngay_ket_thuc'] - xml_df['ngay_bat_dau'])/np.timedelta64(1, 'D')

#     # Create 'loai_khoan_vay' feature
#     xml_df[['loai_khoan_vay']] = ""
#     for i, val in enumerate(xml_df['loantype']):
#         if val == 'Instalments':
#             xml_df['loai_khoan_vay'][i] = 'Vay_Thong_Thuong'
#         elif val == 'NonInstalments':
#             xml_df['loai_khoan_vay'][i] = 'Vay_Thau_Chi'
#         else:
#             xml_df['loai_khoan_vay'][i] = 'The_Tin_Dung'

#     # create 'tenor_khoan_vay' feature based on 'thoi_han_vay' and 'giai_doan_hdv_map'
#     khong_co_khoan_vay = ['RQ', 'RN', 'RF']
#     co_khoan_vay = ['LV', 'TM', 'TA']
#     khoan_vay_hoan_tat = ['TM', 'TA']
#     xml_df[['tenor_khoan_vay']]= ""
#     for i, val in enumerate(xml_df['thoi_han_vay']):
#         if (val <= 360) and (xml_df['giai_doan_hdv_map'][i] in co_khoan_vay):
#             xml_df['tenor_khoan_vay'][i] = "ngan_han"
#         elif (val <=1800) and (xml_df['giai_doan_hdv_map'][i] in co_khoan_vay):
#             xml_df['tenor_khoan_vay'][i] = "trung_han"
#         elif (val > 1800) and (xml_df['giai_doan_hdv_map'][i] in co_khoan_vay):
#             xml_df['tenor_khoan_vay'][i] = 'dai_han'
#         else:
#             xml_df['tenor_khoan_vay'][i] = "khong_co_khoan_vay"

# get all xml files
folder_xml_path = str(Path(__file__).parent/ "xml")
files = [f for f in glob.glob(folder_xml_path + "/*.xml")]
print(files)

## Tets xml_parse main function
path_xml_file = str(Path(__file__).parent/ "xml/000186042261.xml")
# revoke function
df_all = xml_parse(path_xml_file)
# df_all = preprocess_xml(df_all_pre)
print(df_all)
print(df_all.shape[0])