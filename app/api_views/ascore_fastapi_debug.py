from typing import Optional
from fastapi import FastAPI
from fastapi import status, responses
from fastapi_versioning import version
from pydantic import BaseModel, Field
# from settings import ASCORE_URL, AUTHEN, DMN_DATA_REQUEST   #, app
import json
import requests
import logging
from typing import Union

# import configs
# from utils.parse_json_data import parse_dmn_data_response
# from models.tables.ascore import ascorerisk
# from models.response.ascore import ascorerisk201

app = FastAPI()

# def parse_dmn_data_response(dmn_data_response, list_input):
#     data_parse = {}
#     for k, val in dmn_data_response['result']['dmn-evaluation-result']['dmn-context'].items():
#         if (k in list_input) or (k=='classification') or (k=='ascore_total'):
#             data_parse[k]=val
#     return data_parse

class AscoreRisk(BaseModel):
    app_id: str
    user_name: str
    user_group: str
    age: Optional[int] = Field(..., nullable=True)
    month_of_ocp: Optional[int] = Field(..., nullable=True)
    months_in_total_occupation: Optional[int] = Field(..., nullable=True)
    region: Optional[str] = Field(..., nullable=True)
    industry: Optional[str] = Field(..., nullable=True)
    type_of_house: Optional[str] = Field(..., nullable=True)
    gender: Optional[str] = Field(..., nullable=True)
    verified_income: Optional[int] = Field(..., nullable=True)
    main_income: Optional[int] = Field(..., nullable=True)
    num_CIs_paid: Optional[int] = Field(..., nullable=True)
    num_CIs_approved: Optional[int] = Field(..., nullable=True)
    total_contracts_approved: Optional[int] = Field(..., nullable=True)
    ratio_living_contract: Optional[int] = Field(..., nullable=True)
    total_contracts_rejected: Optional[int] = Field(..., nullable=True)
    total_requires: Optional[int] = Field(..., nullable=True)
    pcb_score: Optional[int] = Field(..., nullable=True)

class AscoreInput():
    # url = ASCORE_URL
    # authen = AUTHEN
    # dmn_data_request = DMN_DATA_REQUEST

    # url = 'http://10.129.28.16:8081/kie-server/services/rest/server/containers/rules_100/dmn'

    # authen = ("kieserver", "kieserver1!")

    # dmn_data_request = {
    #     "model-path": "/kie",
    #     "model-namespace": "fico.risk.ascore",
    #     "model-name": "DMMRiskAscore",
    #     "decision-name": [
    #         "Score_DM001", "Score_DM002", "Score_DM003", "Score_DM004", "Score_DM005", "Score_DM006",  "Score_DM007", "Score_LN001", "Score_LN002", "Score_LN004", "Score_LN003", "Score_LN005", "Score_LN006", "Score_CS007", "ascore_total", "classification"
    #     ]
    #     }

    def __init__(self, **kwargs):
        self.app_id = kwargs['app_id']
        self.user_name = kwargs['user_name']
        self.user_group = kwargs['user_group']
        self.age = kwargs['age']
        self.month_of_ocp = kwargs['month_of_ocp']
        self.months_in_total_occupation = kwargs['months_in_total_occupation']
        self.region = kwargs['region']
        self.industry = kwargs['industry']
        self.type_of_house = kwargs['type_of_house']
        self.gender = kwargs['gender']
        self.verified_income = kwargs['verified_income']
        self.main_income = kwargs['main_income']            
        self.num_CIs_paid = kwargs['num_CIs_paid']
        self.num_CIs_approved = kwargs['num_CIs_approved']
        self.total_contracts_approved = kwargs['total_contracts_approved']
        self.ratio_living_contract = kwargs['ratio_living_contract']
        self.total_contracts_rejected = kwargs['total_contracts_rejected']
        self.total_requires = kwargs['total_requires']
        self.pcb_score = kwargs['pcb_score']

    def glob_var():
        from configs.settings import ASCORE_URL, AUTHEN, DMN_DATA_REQUEST
        url = ASCORE_URL
        authen = AUTHEN
        dmn_data_request = DMN_DATA_REQUEST
        return {'url':url, 'authen':authen, 'dmn_data_request':dmn_data_request}

    def call_drool_api(self):
        from utils.parse_json_data import parse_dmn_data_response
        data = self.__dict__
        request_lst = [k for k in data]
        json_req_var = AscoreInput.glob_var()
        json_req = json_req_var["dmn_data_request"]
        json_req["dmn-context"] = data  # add "dmn-context" field for  parameter of the drool api
        result_dmn = None
        try:
            result_dmn = requests.post(json_req_var["url"], json=json_req, auth = json_req_var["authen"])
            # result_dmn = requests.post(AscoreInput.url, json=json_req, auth = AscoreInput.authen)
            # print ('pass')
        except Exception as e:
            logging.Exception('error when call drool. Cheking input params %s' % str(e))
            raise e
        # print('+++++++++++++++++')
        result = json.loads(result_dmn.text) # json to dict
        result_dmn = parse_dmn_data_response(result, request_lst)
        return result_dmn
            
    @classmethod
    def from_request(cls, request_data):
        return cls(
            app_id = request_data['app_id'],
            user_name = request_data['user_name'],
            user_group = request_data['user_group'],
            age = request_data['age'],
            month_of_ocp = request_data['month_of_ocp'],
            months_in_total_occupation = request_data['months_in_total_occupation'],
            region = request_data['region'],
            industry = request_data['industry'],
            type_of_house = request_data['type_of_house'],
            gender = request_data['gender'],            
            verified_income = request_data['verified_income'],
            main_income = request_data['main_income'],
            num_CIs_paid = request_data['num_CIs_paid'],
            num_CIs_approved = request_data['num_CIs_approved'],
            total_contracts_approved = request_data['total_contracts_approved'],
            ratio_living_contract = request_data['ratio_living_contract'],
            total_contracts_rejected = request_data['total_contracts_rejected'],
            total_requires = request_data['total_requires'],
            pcb_score = request_data['pcb_score']
        )

# POST method
@app.post(
    path="/AscoreRisk",
    description="post params into drool apis and get its result",
    responses={
        status.HTTP_201_CREATED: {
            'model': None,
            # 'model': ascorerisk201
        }
    }
)
@version(1, 1)
async def ascore_dmn_process(model: AscoreRisk):
    body = model.dict()
    ascore_rs = None
    try:
        ascore_rs = AscoreInput.from_request(body).call_drool_api()
    except Exception as e:
        logging.error('%s' % str(e))
        raise e
    print(ascore_rs)
    return responses.JSONResponse(ascore_rs, status_code=status.HTTP_201_CREATED)