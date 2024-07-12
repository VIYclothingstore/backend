import requests

from config import settings


class NovaPostApiClient:
    def __init__(self):
        self.api_url = settings.NOVAPOSHTA_API_SETTINGS["API_POINT"]
        self.api_key = settings.NOVAPOSHTA_API_SETTINGS["NOVAPOSHTA_API_KEY"]

    def get_settlements(self, settlement_name, limit=50, page=1):
        data = {
            "apiKey": self.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName": settlement_name,
                "Limit": str(limit),
                "Page": str(page),
            },
        }
        response = requests.post(url=self.api_url, json=data)

        response.raise_for_status()

        return response.json()
