import requests

from config import settings


class NovaPostApiClient:
    def __init__(self):
        self.api_url = settings.NOVAPOSHTA_API_SETTINGS["API_POINT"]
        self.api_key = settings.NOVAPOSHTA_API_SETTINGS["NOVAPOSHTA_API_KEY"]

    def get_settlements(self, settlement_name, limit=25, page=1):
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

    def get_warehouses(self, settlement_name, warehouse_ref, limit=25, page=1):
        data = {
            "apiKey": self.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "FindByString": "",
                "CityName": settlement_name,
                "Limit": str(limit),
                "Page": str(page),
                "TypeOfWarehouseRef": warehouse_ref,
            },
        }
        response = requests.post(url=self.api_url, json=data)
        response.raise_for_status()
        return response.json()

    def get_warehouse_types(self):
        data = {
            "apiKey": self.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouseTypes",
            "methodProperties": {},
        }
        response = requests.post(url=self.api_url, json=data)
        response.raise_for_status()
        return response.json()

    def search_settlement_streets(self, street_name, ref, limit=25, page=1):
        data = {
            "apiKey": self.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "searchSettlementStreets",
            "methodProperties": {
                "StreetName": street_name,
                "SettlementRef": ref,
                "Limit": str(limit),
                "Page": str(page),
            },
        }
        response = requests.post(url=self.api_url, json=data)
        response.raise_for_status()
        return response.json()
