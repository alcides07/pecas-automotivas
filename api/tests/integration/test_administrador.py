import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from ..factories import AdministradorFactory
from ..helpers import validated_pagination
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_read_administradores(administrador):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('administradores-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_validate_pagination_administradores(administrador):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('administradores-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    
    try:
        assert validated_pagination(response.data) is True
    except (ValueError, KeyError) as e:
        pytest.fail(f"Erro na paginação: {e}")

@pytest.mark.django_db
def test_read_administrador_id(administrador):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    administrador_id = administrador["administrador_data"]["id"]
    
    url = reverse('administradores-detail', kwargs={'pk': administrador_id})
    response = client.get(url)

    administrador_username = administrador["administrador_data"]["username"]

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == administrador_username

@pytest.mark.django_db
def test_create_administrador():
    client = APIClient()

    old_count_administradores = User.objects.filter(is_superuser=True, is_staff=True).count()    
    
    new_administrador = AdministradorFactory.build().__dict__
    new_administrador.pop('id', None) 
    new_administrador.pop('last_login', None) 

    url = reverse('administradores-list')
    response = client.post(url, data=new_administrador)

    new_count_administradores = User.objects.filter(is_superuser=True, is_staff=True).count()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == new_administrador["username"]
    assert response.data["email"] == new_administrador["email"]
    assert new_count_administradores == old_count_administradores + 1
