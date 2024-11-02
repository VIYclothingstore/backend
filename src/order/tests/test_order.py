import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from order.models import BasketItem


@pytest.mark.django_db
def test_user_can_create_basket_if_authorized(api_client, test_user_mark):
    api_client.force_authenticate(user=test_user_mark)
    url = reverse("basket-list")
    response = api_client.post(url)

    assert response.status_code == HTTP_201_CREATED
    assert "basket_id" in response.data
    assert response.data["user_id"] == test_user_mark.id


@pytest.mark.django_db
def test_user_can_create_basket_without_authorization(api_client):
    url = reverse("basket-list")
    response = api_client.post(url)

    assert response.status_code == HTTP_201_CREATED
    assert "basket_id" in response.data
    assert "user_id" not in response.data


@pytest.mark.django_db
def test_user_can_add_product_to_the_basket(
    api_client, test_user_mark, basket, products, colors, sizes, warehouse_items
):
    api_client.force_authenticate(user=test_user_mark)
    url = reverse("basket_item-list", kwargs={"basket_id": basket.id})

    data = {
        "product": products[0].id,
        "color": colors[0].id,
        "size": sizes[1].id,
        "quantity": 1,
    }
    response = api_client.post(url, data=data)

    assert response.status_code == HTTP_201_CREATED, response.data
    assert response.data["product"] == products[0].id
    assert response.data["quantity"] == 1


@pytest.mark.django_db
def test_user_cannot_add_product_to_the_basket_if_it_is_sold(
    api_client, basket, products, colors, sizes, warehouse_items
):
    url = reverse("basket_item-list", kwargs={"basket_id": basket.id})
    data = {
        "product": products[0].id,
        "color": colors[1].id,
        "size": sizes[1].id,
        "quantity": 1,
    }
    response = api_client.post(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Sorry, but this product is out of stock"


@pytest.mark.django_db
def test_user_can_update_quantity_of_products_in_basket(
    api_client, test_user_mark, basket, basket_item, warehouse_items
):
    api_client.force_authenticate(user=test_user_mark)
    url = reverse(
        "basket_item-detail",
        kwargs={"basket_id": basket.id, "basket_item_id": basket_item.id},
    )
    data = {
        "quantity": 3,
        "product": basket_item.product.id,
        "color": basket_item.color.id,
        "size": basket_item.size.id,
    }
    response = api_client.patch(url, data=data)

    assert response.status_code == HTTP_200_OK, response.data
    basket_item.refresh_from_db()
    assert basket_item.quantity == 3


@pytest.mark.django_db
def test_user_cannot_update_quantity_of_products_in_basket_if_insufficient_stock(
    api_client, test_user_mark, basket, basket_item, warehouse_items
):
    api_client.force_authenticate(user=test_user_mark)
    url = reverse(
        "basket_item-detail",
        kwargs={"basket_id": basket.id, "basket_item_id": basket_item.id},
    )
    data = {
        "quantity": 10,
        "product": basket_item.product.id,
        "color": basket_item.color.id,
        "size": basket_item.size.id,
    }
    response = api_client.patch(url, data=data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Sorry, but this product is out of stock"


def test_user_can_remove_product_from_basket(
    api_client, test_user_mark, basket, basket_item
):
    api_client.force_authenticate(user=test_user_mark)
    url = reverse(
        "basket_item-detail",
        kwargs={"basket_id": basket.id, "basket_item_id": basket_item.id},
    )
    response = api_client.delete(url)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert not BasketItem.objects.filter(id=basket_item.id).exists()
