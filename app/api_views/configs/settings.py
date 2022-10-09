from fastapi import FastAPI


# Initial FastAPI app
app = FastAPI()

# Initial for DMN apis
ASCORE_URL = 'http://10.129.28.16:8081/kie-server/services/rest/server/containers/rules_100/dmn'

AUTHEN = ("kieserver", "kieserver1!")

DMN_DATA_REQUEST = {
    "model-path": "/kie",
    "model-namespace": "fico.risk.ascore",
    "model-name": "DMMRiskAscore",
    "decision-name": [
        "Score_DM001", "Score_DM002", "Score_DM003", "Score_DM004", "Score_DM005", "Score_DM006",  "Score_DM007", "Score_LN001", "Score_LN002", "Score_LN004", "Score_LN003", "Score_LN005", "Score_LN006", "Score_CS007", "ascore_total", "classification"
    ]
    }

SQL_ENGINE = ""