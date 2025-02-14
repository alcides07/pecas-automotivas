import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..factories import UserFactory
from ..helpers import login

@pytest.fixture
def user():
    user_factory = UserFactory()
    token = login(user_factory)

    return {
        'access': token['access'],
        'refresh': token['refresh']
    }

@pytest.mark.django_db
def test_read_parts(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('parts-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

