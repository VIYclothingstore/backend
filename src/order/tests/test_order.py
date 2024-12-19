import pytest
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

import users
from order.models import BasketItem


@pytest.mark.django_db
def test_create_baskets_for_user(
    api_client,
    test_user_mark,
):
    api_client.force_authenticate(user=test_user_mark)
    response = api_client.post(
        reverse("basket-list"),
    )
    assert response.status_code == HTTP_201_CREATED
    assert "basket_id" in response.data
    assert response.data["user_id"] == test_user_mark.id


@pytest.mark.django_db
def test_create_baskets_for_anonim(
    api_client,
):
    response = api_client.post(
        reverse("basket-list"),
    )
    assert response.status_code == HTTP_201_CREATED
    assert "basket_id" in response.data
    assert "user_id" not in response.data


@pytest.mark.django_db
def tests_add_product_to_basket(
    api_client,
    basket,
    products,
    colors,
    sizes,
    warehouse_items,
    test_user_mark,
):
    if users:
        api_client.force_authenticate(user=test_user_mark)
    path = reverse("basket_item-list", kwargs={"basket_id": basket.id})
    basket_data = {
        "product": products[0].id,
        "color": colors[0].id,
        "size": sizes[1].id,
        "quantity": 1,
    }
    response = api_client.post(path, data=basket_data)
    assert response.status_code == HTTP_201_CREATED, response.data
    assert response.data["product"] == products[0].id
    assert response.data["quantity"] == 1


@pytest.mark.django_db
def test_user_add_product_to_the_basket(
    api_client,
    basket,
    products,
    colors,
    sizes,
    warehouse_items,
    test_user_mark,
):
    tests_add_product_to_basket(
        api_client,
        basket,
        products,
        colors,
        sizes,
        warehouse_items,
        test_user_mark,
    )


@pytest.mark.django_db
def test_anonim_add_product_to_the_basket(
    api_client,
    basket,
    products,
    colors,
    sizes,
    warehouse_items,
    test_user_mark=None,
):
    tests_add_product_to_basket(
        api_client,
        basket,
        products,
        colors,
        sizes,
        warehouse_items,
        test_user_mark=None,
    )


@pytest.mark.django_db
def test_cannot_add_product_to_basket_if_sold(
    api_client,
    basket,
    products,
    colors,
    sizes,
    warehouse_items,
    test_user_mark,
):
    if users:
        api_client.force_authenticate(user=test_user_mark)

    path = reverse("basket_item-list", kwargs={"basket_id": basket.id})
    basket_data = {
        "product": products[0].id,
        "color": colors[1].id,
        "size": sizes[1].id,
        "quantity": 1,
    }
    response = api_client.post(path, data=basket_data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Sorry, but this product is out of stock"


@pytest.mark.django_db
def test_user_cannot_add_product_to_basket_if_sold(
    api_client,
    basket,
    products,
    colors,
    sizes,
    warehouse_items,
    test_user_mark,
):
    test_cannot_add_product_to_basket_if_sold(
        api_client,
        basket,
        products,
        colors,
        sizes,
        warehouse_items,
        test_user_mark,
    )


@pytest.mark.django_db
def test_anonim_cannot_add_product_to_basket_if_sold(
    api_client,
    basket,
    products,
    colors,
    sizes,
    warehouse_items,
    test_user_mark=None,
):
    test_cannot_add_product_to_basket_if_sold(
        api_client,
        basket,
        products,
        colors,
        sizes,
        warehouse_items,
        test_user_mark=None,
    )


@pytest.mark.django_db
def test_update_quantity_of_products_in_basket(
    api_client,
    basket,
    basket_item,
    warehouse_items,
    test_user_mark,
):
    if users:
        api_client.force_authenticate(user=test_user_mark)
    path = reverse(
        "basket_item-detail",
        kwargs={"basket_id": basket.id, "basket_item_id": basket_item.id},
    )
    basket_data = {
        "quantity": 3,
        "product": basket_item.product.id,
        "color": basket_item.color.id,
        "size": basket_item.size.id,
    }
    response = api_client.patch(path, data=basket_data)

    assert response.status_code == HTTP_200_OK, response.data
    basket_item.refresh_from_db()
    assert basket_item.quantity == 3


@pytest.mark.django_db
def test_user_update_quantity_of_products_in_basket(
    api_client,
    basket,
    basket_item,
    warehouse_items,
    test_user_mark,
):
    test_update_quantity_of_products_in_basket(
        api_client,
        basket,
        basket_item,
        warehouse_items,
        test_user_mark,
    )


@pytest.mark.django_db
def test_anonim_update_quantity_of_products_in_basket(
    api_client,
    basket,
    basket_item,
    warehouse_items,
    test_user_mark=None,
):
    test_update_quantity_of_products_in_basket(
        api_client,
        basket,
        basket_item,
        warehouse_items,
        test_user_mark=None,
    )


@pytest.mark.django_db
def test_out_of_stock(
    api_client,
    basket,
    basket_item,
    warehouse_items,
    test_user_mark,
):
    if users:
        api_client.force_authenticate(user=test_user_mark)
    path = reverse(
        "basket_item-detail",
        kwargs={"basket_id": basket.id, "basket_item_id": basket_item.id},
    )
    basket_data = {
        "quantity": 10,
        "product": basket_item.product.id,
        "color": basket_item.color.id,
        "size": basket_item.size.id,
    }
    response = api_client.patch(path, data=basket_data)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Sorry, but this product is out of stock"


@pytest.mark.django_db
def test_user_out_of_stock(
    api_client,
    basket,
    basket_item,
    warehouse_items,
    test_user_mark,
):
    test_out_of_stock(
        api_client,
        basket,
        basket_item,
        warehouse_items,
        test_user_mark,
    )


@pytest.mark.django_db
def test_anonim_out_of_stock(
    api_client,
    basket,
    basket_item,
    warehouse_items,
    test_user_mark=None,
):
    test_out_of_stock(
        api_client,
        basket,
        basket_item,
        warehouse_items,
        test_user_mark=None,
    )


def test_del_product_from_basket(
    api_client,
    basket,
    basket_item,
    test_user_mark,
):
    if users:
        api_client.force_authenticate(user=test_user_mark)

    path = reverse(
        "basket_item-detail",
        kwargs={"basket_id": basket.id, "basket_item_id": basket_item.id},
    )
    response = api_client.delete(path)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert not BasketItem.objects.filter(id=basket_item.id).exists()


@pytest.mark.django_db
def test_user_del_product_from_basket(
    api_client,
    basket,
    basket_item,
    test_user_mark,
):
    test_del_product_from_basket(
        api_client,
        basket,
        basket_item,
        test_user_mark,
    )


@pytest.mark.django_db
def test_anonim_del_product_from_basket(
    api_client,
    basket,
    basket_item,
    test_user_mark=None,
):
    test_del_product_from_basket(
        api_client,
        basket,
        basket_item,
        test_user_mark=None,
    )
