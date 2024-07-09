from rest_framework.response import Response
from rest_framework.views import APIView

from delivery.nova_post_api_client import NovaPostApiClient


class NovaPoshtaCityView(APIView):
    def get(self, request, city_name):
        """
        API endpoint to retrieve information about a city using Nova Poshta API.

        Args:
            request (Request): The incoming HTTP request.
            city_name (str): The name of the city to search for.
        """

        limit = request.query_params.get("limit", 50)
        page = request.query_params.get("page", 2)

        client = NovaPostApiClient()
        cities = client.get_city(city_name, limit, page)

        return Response(data=cities)
