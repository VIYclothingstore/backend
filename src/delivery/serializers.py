from rest_framework.response import Response
from rest_framework.views import APIView

from delivery.nova_post_api_client import NovaPostApiClient


class NovaPostaSettlementsView(APIView):
    def get(self, request, settlement_name):
        """
        An API endpoint for receiving information about settlements using the Nova Posta API.
        """
        limit = request.query_params.get("limit", 50)
        page = request.query_params.get("page", 1)

        client = NovaPostApiClient()
        cities = client.get_settlements(settlement_name, limit, page)

        return Response(data=cities)
