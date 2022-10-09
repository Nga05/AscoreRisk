import requests
import json


username="kieserver"
password="kieserver1!"

url = "http://10.129.28.16:8081/kie-server/services/rest/server/containers/rules_100/dmn"
rs = requests.get(url, auth=(username, password))
# print(rs.status_code)


input_dt = {
    "model-path": "/kie",
    "model-namespace": "fico.risk.ascore",
    "model-name": "DMMRiskAscore",
    "decision-name": [
        "Score_DM001", "Score_DM002", "Score_DM003", "Score_DM004", "Score_DM005", "Score_DM006",  "Score_DM007", "Score_LN001", "Score_LN002", "Score_LN004", "Score_LN003", "Score_LN005", "Score_LN006", "Score_CS007", "ASCORE_TOTAL", "CLASSIFICATION"
    ],
    "dmn-context": {
        "age": 26,
        "month_of_ocp": 30,
        "region": "South",
        "industry": "T-Manufacturing",
        "type_of_house": "Other",
        "gender": "Female",
        "verified_income": 18000000,
        "num_CIs_paid": 0,
        "num_CIs_approved": 0,
        "total_contracts_approved": 7,
        "ratio_living_contract": 0.86,
        "total_contracts_rejected": 0,
        "total_requires": 4,
        "pcb_score": 380
    }
}

x = requests.post(url, json=input_dt, auth=(username, password)) #, json=input_dt, auth=None
response = json.loads(x.text)
# print(x.text)

for k, val in response['result']['dmn-evaluation-result']['dmn-context'].items():
    print(k, val)