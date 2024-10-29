import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_can_retrieve_the_product(api_client, products):
    product = products[0]
    url = reverse("product-retrieve", kwargs={"id": product.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == product.id


@pytest.mark.django_db
def test_user_can_get_list_of_products(api_client, products):
    url = reverse("product-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) > 0
    assert response.data[0]["id"] == products[0].id
    assert response.data[0]["title"] == products[0].title


@pytest.mark.django_db
def test_user_can_get_products_available_in_stock(api_client, warehouse_item):
    url = reverse(
        "product-available-stock",
        kwargs={
            "product_id": warehouse_item.product.id,
            "color_id": warehouse_item.color.id,
            "size_id": warehouse_item.size.id,
        },
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_user_can_get_products_that_are_sold_out_from_stock(
    api_client, sold_warehouse_item
):
    url = reverse(
        "product-available-stock",
        kwargs={
            "product_id": sold_warehouse_item.product.id,
            "color_id": sold_warehouse_item.color.id,
            "size_id": sold_warehouse_item.size.id,
        },
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0


@pytest.mark.django_db
def test_user_can_sort_by_price_ascending(api_client, products):
    url = reverse("product-sorting")
    response = api_client.get(url, {"sort": "price_asc"})

    assert response.status_code == status.HTTP_200_OK
    prices = [product["price"] for product in response.data]
    assert prices == sorted(prices)


@pytest.mark.django_db
def test_sort_by_price_descending(api_client, products):
    url = reverse("product-sorting")
    response = api_client.get(url, {"sort": "price_desc"})

    assert response.status_code == status.HTTP_200_OK
    prices = [product["price"] for product in response.data]
    assert prices == sorted(prices, reverse=True)


@pytest.mark.django_db
def test_user_can_sort_by_popularity(api_client, products):
    url = reverse("product-sorting")
    response = api_client.get(url, {"sort": "popular"})

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_user_can_search_product_by_gender(api_client, products):
    url = reverse("product-search")
    response = api_client.get(url, {"gender": "Men"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_user_can_search_product_by_category(api_client, products):
    url = reverse("product-search")
    response = api_client.get(url, {"category": "Shirts"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_search_product_by_title(api_client, products):
    url = reverse("product-search")
    response = api_client.get(url, {"title": "T-shirt"})

    print("Response Data:", response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_search_product_by_description(api_client, products):
    url = reverse("product-search")
    response = api_client.get(url, {"description": "Cool T-shirt"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_search_product_by_size(api_client, products):
    url = reverse("product-search")
    response = api_client.get(url, {"size": "L"})

    print("Response Data:", response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_search_product_by_color(api_client, products):
    url = reverse("product-search")
    response = api_client.get(url, {"color": "Black"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_filter_by_gender(api_client, products):
    url = reverse("filter-products")
    response = api_client.get(url, {"gender": "Men"})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_user_can_filter_by_size(api_client, products):
    url = reverse("filter-products")
    response = api_client.get(url, {"sizes": ["L"]})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_filter_by_price_range(api_client, products):
    url = reverse("filter-products")
    response = api_client.get(url, {"min_price": 350, "max_price": 500})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_user_can_filter_by_color(api_client, products):
    url = reverse("filter-products")
    response = api_client.get(url, {"colors": ["Black"]})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_can_filter_several_parameters(api_client, products):
    url = reverse("filter-products")
    response = api_client.get(
        url,
        {
            "sizes": ["L"],
            "min_price": 400,
            "max_price": 500,
            "colors": ["Red"],
            "gender": "Men",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_cannot_found_products(api_client, products):
    url = reverse("filter-products")
    response = api_client.get(url, {"sizes": ["M"], "colors": ["Red"]})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
