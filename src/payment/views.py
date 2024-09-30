from django.http import HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from config import settings
from config.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY
from delivery.models import PAYMENT_OK, Order
from payment.liqpay_client import LiqPay


class PayCallbackView(View):
    @method_decorator(csrf_exempt, name="dispatch")
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        data = request.POST.get("data")
        signature = request.POST.get("signature")
        sign = liqpay.str_to_sign(LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY)
        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            order_id = response.get("order_id")
            if order_id:
                try:
                    order = Order.objects.get(pk=order_id)
                    order.status = PAYMENT_OK
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponseNotFound("Order not found")

            return HttpResponse(request, response)


class CheckPaymentStatusView(APIView):
    def post(self, request):
        try:
            order_id = request.data.get("order_id")
            if not order_id:
                return Response(
                    data=dict(msg="Missing order_id in request data"),
                    status=HTTP_400_BAD_REQUEST,
                )
            liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
            params = {
                "action": "status",
                "version": "3",
                "order_id": str(order_id),
            }
            response = liqpay.api("request", params)
            return Response(
                data=dict(response),
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data=dict(
                    msg=str(e),
                    status=HTTP_500_INTERNAL_SERVER_ERROR,
                )
            )
