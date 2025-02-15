import pytest
import jwt
import time
from datetime import datetime, timedelta
from django.urls import reverse
from pecas_automotivas import settings
from django.contrib.auth.models import User
from ..factories import UserFactory
from ..helpers import validated_pagination
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_read_users(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('users-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_validate_pagination_users(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('users-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    
    try:
        assert validated_pagination(response.data) is True
    except (ValueError, KeyError) as e:
        pytest.fail(f"Erro na paginação: {e}")

@pytest.mark.django_db
def test_read_user_id(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    user_id = user["user_data"]["id"]
    
    url = reverse('users-detail', kwargs={'pk': user_id})
    response = client.get(url)

    user_username = user["user_data"]["username"]

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == user_username

@pytest.mark.django_db
def test_create_user():
    client = APIClient()

    old_count_users = User.objects.count()
    new_user = UserFactory.build().__dict__
    new_user.pop('id', None) 
    new_user.pop('last_login', None) 

    url = reverse('users-list')
    response = client.post(url, data=new_user)

    new_count_users = User.objects.count()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == new_user["username"]
    assert response.data["email"] == new_user["email"]
    assert new_count_users == old_count_users + 1

@pytest.mark.django_db
def test_validate_jwt(user):
    access_token = user['access']

    try:
        _ = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        pytest.fail("Token JWT expirou")
    except jwt.InvalidTokenError:
        pytest.fail("Token JWT é inválido")

@pytest.mark.django_db
def test_expired_jwt():
    payload = {
        'user_id': 1,
        'exp': datetime.now() + timedelta(seconds=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    
    time.sleep(2)

    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])