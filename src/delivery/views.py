from abc import ABC, abstractmethod

from rest_framework.response import Response
from rest_framework.views import APIView

from delivery.nova_post_api_client import NovaPostApiClient


class NovaPostView(APIView, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 1
        self.limit = 25
        self.client = NovaPostApiClient()

    @abstractmethod
    def _get_data(self, **kwargs):
        pass

    def get(self, request, **kwargs):
        self.limit = request.query_params.get("limit", self.limit)
        self.page = request.query_params.get("page", self.page)
        return Response(data=self._get_data(**kwargs))


class SettlementsView(NovaPostView):
    def _get_data(self, settlement_name, **kwargs):
        return self.client.get_settlements(settlement_name, self.limit, self.page)


class WarehousesView(NovaPostView):
    def _get_data(self, settlement_name, warehouse_ref, **kwargs):
        return self.client.get_warehouses(
            settlement_name, warehouse_ref, self.limit, self.page
        )


class WarehouseTypeView(NovaPostView):
    def _get_data(self, **kwargs):
        return self.client.get_warehouse_types()


class AddressesView(NovaPostView):
    def _get_data(self, street_name, ref, **kwargs):
        return self.client.search_settlement_streets(
            street_name, ref, self.limit, self.page
        )
