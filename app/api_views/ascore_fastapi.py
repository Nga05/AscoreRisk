from typing import List, Optional, Union
from fastapi import status, responses, Body
from pydantic import BaseModel
# from api_views.configs.settings import ASCORE_URL, AUTHEN, DMN_DATA_REQUEST, app
# from api_views.utils.parse_json_data import parse_dmn_data_response
# from api_views.utils.xml_parse_bs4 import AScoreData
from configs.settings import ASCORE_URL, AUTHEN, DMN_DATA_REQUEST, app
# from utils.parse_json_data import parse_dmn_data_response
from utils.xml_parse_bs4 import AScoreData
from fastapi_versioning import version
# from api_views.models.response.ascore import ascorerisk201
from models.response.ascore import ascorerisk201
from pathlib import Path
from fastapi import FastAPI
import json
import requests
import logging
import random
import glob
import numpy as np
import pandas as pd
import json
import re


# Initial FastAPI app
app = FastAPI()

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64) \
            or isinstance(obj, np.int8) \
            or isinstance(obj, np.int16) \
            or isinstance(obj, np.int32) \
            or isinstance(obj, np.int128) \
            or isinstance(obj, np.int256):
            return int(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class AscoreInput:
    url = ASCORE_URL
    authen = AUTHEN
    dmn_data_request = DMN_DATA_REQUEST

    def __init__(
        self, 
        app_id: str, 
        user_name: Union[str, None], 
        user_group: Union[str, None], 
        age: Union[int, None], 
        month_of_ocp: Union[int, None], 
        months_in_total_occupation: Union[int, None], 
        region: Union[str, None], 
        industry: Union[str, None], 
        type_of_house: Union[str, None],
        gender: Union[str, None],
        verified_income: Union[int, None],
        main_income: Union[int, None],
        num_CIs_paid = Union[int, None],
        num_CIs_approved = Union[int, None],
        total_contracts_approved = Union[int, None],
        ratio_living_contract = Union[float, None],
        total_contracts_rejected = Union[int, None],
        total_requires = Union[int, None],
        pcb_score = Union[int, None]
    ):
        self.app_id = app_id
        self.user_name = user_name
        self.user_group = user_group
        self.age = age
        self.month_of_ocp = month_of_ocp
        self.months_in_total_occupation = months_in_total_occupation
        self.region = region
        self.industry = industry
        self.type_of_house = type_of_house
        self.gender = gender
        self.verified_income = verified_income
        self.main_income = main_income
        self.num_CIs_paid = num_CIs_paid
        self.num_CIs_approved = num_CIs_approved
        self.total_contracts_approved = total_contracts_approved
        self.ratio_living_contract = ratio_living_contract
        self.total_contracts_rejected = total_contracts_rejected
        self.total_requires = total_requires
        self.pcb_score = pcb_score
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data['app_id'],
            data['user_name'],
            data['user_group'],
            data['age'],
            data['month_of_ocp'],
            data['months_in_total_occupation'],
            data['region'],
            data['industry'],
            data['type_of_house'],
            data['gender'],
            data['verified_income'],
            data['main_income'],
            data['num_CIs_paid'],
            data['num_CIs_approved'],
            data['total_contracts_approved'],
            data['ratio_living_contract'],
            data['total_contracts_rejected'],
            data['total_requires'],
            data['pcb_score']
        )

    def call_drool_api(self):
        data = self.__dict__
        request_lst = [k for k in data]
        json_req = AscoreInput.dmn_data_request
        json_req["dmn-context"] = data  # add "dmn-context" field for  parameter of the drool api
        json_req = json.dumps(json_req, cls=NpEncoder)
        result_dmn = None
        try:
            result_dmn = requests.post(
                AscoreInput.url,
                json = json.loads(json_req),
                auth = AscoreInput.authen
            )
            print ('pass')
        except Exception as e:
            logging.getLogger('error when call drool. Cheking input params %s' % str(e))
            raise e
        result = json.loads(result_dmn.text)  # json to dict
        result_dmn = ProcessResponse.parse_dmn_data_response(result, request_lst)
        return result_dmn


class ProcessResponse:
    def __init__(self, dmn_data_response: dict, list_input: List) -> None:
        self.dmn_data_response = dmn_data_response
        self.list_input = list_input

    def parse_dmn_data_response(dmn_data_response, list_input):
        data_parse = {}
        for k, val in dmn_data_response['result']['dmn-evaluation-result']['dmn-context'].items():
            if (k in list_input) or (k=='classification') or (k=='ascore_total'):
                data_parse[k]=val
        return data_parse


class AscoreRisk(BaseModel):
    app_id: Optional[str] = Body(default=None)
    user_name: Optional[str] = Body(default=None)
    user_group: Optional[str] = Body(default=None)
    age: Union[int, None] = Body(..., nullable=True)
    month_of_ocp: Union[int, None] = Body(..., nullable=True)
    months_in_total_occupation: Union[int, None] = Body(..., nullable=True)
    region: Union[str, None] = Body(..., nullable=True)
    industry: Union[str, None] = Body(..., nullable=True)
    type_of_house: Union[str, None] = Body(..., nullable=True)
    gender: Union[str, None] = Body(..., nullable=True)
    verified_income: Union[int, None] = Body(..., nullable=True)
    main_income: Union[int, None] = Body(..., nullable=True)
    num_CIs_paid: Union[int, None] = Body(..., nullable=True)
    num_CIs_approved: Union[int, None] = Body(..., nullable=True)
    total_contracts_approved: Union[int, None] = Body(..., nullable=True)
    ratio_living_contract: Union[int, None] = Body(..., nullable=True)
    total_contracts_rejected: Union[int, None] = Body(..., nullable=True)
    total_requires: Union[int, None] = Body(..., nullable=True)
    pcb_score: Union[int, None] = Body(..., nullable=True)


class Backtest(AScoreData):  # AscoreInput
    user_name = "username_test"
    user_group = "username_test"
    regions = ["Mekong", "North", "South", "Central", None]
    region = random.choice(regions)
    type_of_houses = ["Rented", "other", None]
    type_of_house = random.choice(type_of_houses)


    def __init__(self, xmlfilepath, dbfilepath):
        self.xmlfilepath = xmlfilepath
        self.dbfilepath = dbfilepath

    def save_drool(self):
        ascore_data = self.generate_input()
        body = ascore_data
        ascore_js = AscoreInput.from_dict(body).call_drool_api()
        return ascore_js

    def generate_input(self) -> Union[AscoreRisk, None]:
        ascore_data = AScoreData.todataframe(self.xmlfilepath, self.dbfilepath)
        df_ascore = ascore_data.calc_all()
        
        # get from random
        AscoreRisk.user_name = self.user_name
        AscoreRisk.user_group = self.user_group
        AscoreRisk.region = self.region
        AscoreRisk.type_of_house = self.type_of_house

        # get from Database / parse xml file
        if df_ascore.empty:
            AscoreRisk.app_id = None
            AscoreRisk.age = None
            AscoreRisk.month_of_ocp = None
            AscoreRisk.months_in_total_occupation = None
            AscoreRisk.industry = None
            AscoreRisk.gender = None
            AscoreRisk.verified_income = None
            AscoreRisk.main_income = None
            AscoreRisk.num_CIs_paid = None
            AscoreRisk.num_CIs_approved = None
            AscoreRisk.total_contracts_approved = None
            AscoreRisk.ratio_living_contract = None
            AscoreRisk.total_contracts_rejected = None
            AscoreRisk.total_requires = None
        else:
            AscoreRisk.app_id = df_ascore['APPLICATION_NUMBER'].values[0]
            AscoreRisk.age = df_ascore['AGE'].values[0]
            AscoreRisk.month_of_ocp = df_ascore['MONTHS_IN_OCCUPATION'].values[0]
            AscoreRisk.months_in_total_occupation = df_ascore['MONTHS_IN_OCCUPATION'].values[0]
            AscoreRisk.industry = df_ascore['INDUSTRY'].values[0]
            AscoreRisk.gender = df_ascore['GENDER'].values[0]
            AscoreRisk.verified_income = df_ascore['VERIFY_INCOME'].values[0]
            AscoreRisk.main_income = df_ascore['MAIN_INCOME'].values[0]
            AscoreRisk.num_CIs_paid = df_ascore["num_CIs_paid"].values[0]
            AscoreRisk.num_CIs_approved = df_ascore["num_CIs_approved"].values[0]
            AscoreRisk.total_contracts_approved = df_ascore["total_contracts_approved"].values[0]
            AscoreRisk.ratio_living_contract = df_ascore["ratio_living_contract"].values[0]
            AscoreRisk.total_contracts_rejected = df_ascore["total_contracts_rejected"].values[0]
            AscoreRisk.total_requires = df_ascore["total_requires"].values[0]
            AscoreRisk.pcb_score = df_ascore["pcb_score"].values[0]

        body = {
            "app_id": AscoreRisk.app_id,
            "user_name": AscoreRisk.user_name,
            "user_group": AscoreRisk.user_group,
            "age": AscoreRisk.age,
            "month_of_ocp": AscoreRisk.month_of_ocp,
            "months_in_total_occupation": AscoreRisk.months_in_total_occupation,
            "region": AscoreRisk.region,
            "industry": AscoreRisk.industry,
            "type_of_house": AscoreRisk.type_of_house,
            "gender": AscoreRisk.gender,
            "verified_income": AscoreRisk.verified_income,
            "main_income": AscoreRisk.main_income,
            "num_CIs_paid": AscoreRisk.num_CIs_paid,
            "num_CIs_approved": AscoreRisk.num_CIs_approved,
            "total_contracts_approved": AscoreRisk.total_contracts_approved,
            "ratio_living_contract": AscoreRisk.ratio_living_contract,
            "total_contracts_rejected": AscoreRisk.total_contracts_rejected,
            "total_requires": AscoreRisk.total_requires,
            "pcb_score": AscoreRisk.pcb_score
        }
        return body


# API
# POST method
@app.post(
    path="/AscoreRisk",
    description="Insert data into AscoreRisk table",
    responses={
        status.HTTP_201_CREATED: {
            'model': ascorerisk201
        }
    }
)
@version(1, 1)
async def ascore_dmn_process(data_model: AscoreRisk):
    body = data_model.dict()
    ascore_rs = None
    try:
        ascore_rs = AscoreInput.from_dict(body).call_drool_api()
    except Exception as e:
        logging.getLogger('%s' % str(e))
        raise e
    # insert output of drool api into database model here...
    print((ascore_rs))
    return responses.JSONResponse(ascore_rs, status_code=status.HTTP_201_CREATED)
