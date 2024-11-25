import uuid

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from users.models import ConfirmationUserEmail, User

User = get_user_model()


@pytest.mark.django_db
def test_user_registration(api_client, user_data):
    url = reverse("user-registration")

    response = api_client.post(url, user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="kolia.chayun@gmail.com").exists()


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        email="superuser@example.com", password="supersecurepassword"
    )

    assert user.email == "superuser@example.com"
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_active is True


@pytest.mark.django_db
def test_user_can_delete_own_account(api_client, test_user_mark):
    api_client.force_authenticate(user=test_user_mark)

    url = reverse("user-retrieve-update-destroy", kwargs={"pk": test_user_mark.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(email="testuser@example.com").exists()


@pytest.mark.django_db
def test_user_can_update_phone_number(api_client, test_user_mark):
    api_client.force_authenticate(user=test_user_mark)

    update_data = {
        "phone_number": "+380962790574",
    }

    url = reverse("user-retrieve-update-destroy", kwargs={"pk": test_user_mark.pk})
    response = api_client.patch(url, update_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    test_user_mark.refresh_from_db()
    assert test_user_mark.phone_number == "+380962790574"


@pytest.mark.django_db
def test_user_can_update_own_data(api_client, test_user_mark):

    api_client.force_authenticate(user=test_user_mark)

    url = reverse("user-retrieve-update-destroy", kwargs={"pk": test_user_mark.id})

    new_data = {
        "email": "new_email@gmail.com",
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "surname": "NewSurname",
        "phone_number": "+380975645638",
    }

    response = api_client.put(url, new_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == new_data["email"]
    assert response.data["first_name"] == new_data["first_name"]
    assert response.data["last_name"] == new_data["last_name"]
    assert response.data["surname"] == new_data["surname"]
    assert response.data["phone_number"] == new_data["phone_number"]


@pytest.mark.django_db
def test_user_can_view_info_about_his_account(api_client, test_user_mark):
    api_client.force_authenticate(user=test_user_mark)

    url = reverse("user-view")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == test_user_mark.id
    assert response.data["email"] == test_user_mark.email
    assert response.data["first_name"] == test_user_mark.first_name
    assert response.data["last_name"] == test_user_mark.last_name
    assert response.data["surname"] == test_user_mark.surname
    assert response.data["phone_number"] == test_user_mark.phone_number


@pytest.mark.django_db
def test_token_obtain_pair_success(api_client, test_user_jon):
    url = reverse("user-login")

    data = {"email": test_user_jon.email, "password": "qwertyuiop"}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
    assert isinstance(response.data["access"], str)
    assert isinstance(response.data["refresh"], str)


@pytest.mark.django_db
def test_user_can_activation_account(api_client, test_user_mark):

    activation_key = uuid.uuid4()
    ConfirmationUserEmail.objects.create(user=test_user_mark, token=activation_key)

    url = reverse("confirm-email", args=[activation_key])

    assert not test_user_mark.is_active

    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["msg"] == "Congratulations, user activated successfully."

    test_user_mark.refresh_from_db()
    assert test_user_mark.is_active


@pytest.mark.django_db
def test_user_can_logout(api_client, test_user_mark):
    api_client.force_authenticate(user=test_user_mark)

    url = reverse("user-logout")
    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["msg"] == "Successfully logged out!"


@pytest.mark.django_db
def test_user_cannot_registration_with_existing_email(api_client, user_data):
    url = reverse("user-registration")

    api_client.post(url, user_data)

    response_second_registration = api_client.post(url, user_data)

    assert response_second_registration.status_code == status.HTTP_400_BAD_REQUEST
    assert response_second_registration.data["email"] == [
        "user with this email already exists."
    ]


@pytest.mark.django_db
def test_user_cannot_registration_with_non_matching_passwords(api_client, user_data):
    url = reverse("user-registration")

    user_data["repeat_password"] = "zxcvbnm"

    response = api_client.post(url, user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"] == ["Passwords do not match."]


@pytest.mark.django_db
def test_user_cannot_registration_with_short_password(api_client, user_data):
    url = reverse("user-registration")

    user_data["password"] = "123"
    user_data["repeat_password"] = "123"

    response = api_client.post(url, user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"] == [
        "The password must consist of any characters and have a length of at least 6"
    ]


@pytest.mark.django_db
def test_user_cannot_login_with_incorrect_password(api_client, test_user_jon):
    url = reverse("user-login")

    response = api_client.post(
        url, {"email": test_user_jon.email, "password": "zxcvbnm"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        response.data["detail"] == "No active account found with the given credentials"
    )
