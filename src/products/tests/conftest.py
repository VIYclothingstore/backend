import pytest
from rest_framework.test import APIClient

from products.models import (
    IN_STOCK,
    SOLD,
    Category,
    Color,
    ProductItem,
    ProductSize,
    WarehouseItem,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def categories():
    categories = [
        Category(gender="Women", sub_category="Shirts"),
        Category(gender="Men", sub_category="Caps"),
        Category(gender="Men", sub_category="Shorts"),
    ]

    return Category.objects.bulk_create(categories)


@pytest.fixture
def colors():
    colors = [
        Color(title="Black"),
        Color(title="White"),
        Color(title="Red"),
    ]

    return Color.objects.bulk_create(colors)


@pytest.fixture
def sizes():
    sizes = [
        ProductSize(value="S"),
        ProductSize(value="M"),
        ProductSize(value="L"),
    ]

    return ProductSize.objects.bulk_create(sizes)


@pytest.fixture
def products(categories, colors, sizes):
    product1 = ProductItem.objects.create(
        category=categories[0], title="T-shirt", description="Cool T-shirt", price=350
    )
    product1.color.add(colors[0])
    product1.size.add(sizes[1])

    product2 = ProductItem.objects.create(
        category=categories[1], title="Cap", description="Cool Cap", price=499
    )
    product2.color.add(colors[2])
    product2.size.add(sizes[2])

    product3 = ProductItem.objects.create(
        category=categories[2], title="Shorts", description="Cool Shorts", price=750
    )
    product3.color.add(colors[1])
    product3.size.add(sizes[0])

    return [product1, product2, product3]


@pytest.fixture
def warehouse_item(products, colors, sizes):
    return WarehouseItem.objects.create(
        product=products[0],
        color=colors[0],
        size=sizes[1],
        status=IN_STOCK,
    )


@pytest.fixture
def sold_warehouse_item(products, colors, sizes):
    return WarehouseItem.objects.create(
        product=products[1],
        color=colors[2],
        size=sizes[2],
        status=SOLD,
    )
