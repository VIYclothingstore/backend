from rest_framework.response import Response
from rest_framework.views import APIView

from delivery.nova_post_api_client import NovaPostApiClient


class NovaPostSettlementsView(APIView):
    def get(self, request, settlement_name):
        """
        Getting information about settlements by name.
        """
        limit = request.query_params.get("limit", 50)
        page = request.query_params.get("page", 1)
        client = NovaPostApiClient()
        cities = client.get_settlements(settlement_name, limit, page)
        return Response(data=cities)


class NovaPostWarehousesView(APIView):
    def get(self, request, warehouse_id, settlement_name):
        """
        Getting information about warehouses in a certain city.
        """
        limit = request.query_params.get("limit", 20)
        page = request.query_params.get("page", 1)
        client = NovaPostApiClient()
        warehouses = client.get_warehouses(warehouse_id, settlement_name, limit, page)
        return Response(data=warehouses)


class NovaPostAddressesView(APIView):
    def get(self, request, street_name, ref):
        """
        Getting information about streets in a certain city.
        """
        limit = request.query_params.get("limit", 20)
        page = request.query_params.get("page", 1)
        client = NovaPostApiClient()
        streets = client.search_settlement_streets(street_name, ref, limit, page)
        return Response(data=streets)
