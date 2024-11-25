import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "kolia.chayun@gmail.com",
        "password": "qwertyuiop",
        "repeat_password": "qwertyuiop",
        "first_name": "Kolya",
        "last_name": "Chaiun",
        "surname": "Andreevich",
        "phone_number": "+380962790573",
    }


@pytest.fixture
def test_user_mark(db):
    return User.objects.create_user(
        email="mark007@gmail.com",
        password="qwertyuiop",
        first_name="Mark",
        last_name="Markovich",
        surname="Markovich",
        phone_number="+380962790573",
    )


@pytest.fixture
def test_user_jon(db):
    return User.objects.create_user(
        email="jon.jones@gmail.com",
        password="qwertyuiop",
        first_name="Jon",
        last_name="Jon",
        surname="Jon",
        phone_number="+380962790579",
        is_active=True,
    )
