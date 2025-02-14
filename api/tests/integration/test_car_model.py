import pytest
from django.urls import reverse
from api.models import CarModel
from ..helpers import validated_pagination
from rest_framework.test import APIClient
from rest_framework import status
from api.tests.factories import CarModelFactory

@pytest.fixture
def create_fifty_car_models():
    for _ in range(50):
       CarModelFactory()

@pytest.mark.django_db
def test_read_car_models(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('car models-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_validate_pagination_car_models(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('car models-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    
    try:
        assert validated_pagination(response.data) is True
    except (ValueError, KeyError) as e:
        pytest.fail(f"Erro na paginação: {e}")

@pytest.mark.django_db
def test_read_car_models_with_filter_name(user, car_model, create_fifty_car_models):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('car models-list')

    short_car_model_name = car_model.name[:5]
    response = client.get(url, {'name': short_car_model_name})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    car_model_found = False
    for item in results:
        if item['id'] == car_model.id and item['name'].lower() == car_model.name.lower():
            car_model_found = True
            break

    assert car_model_found is True

@pytest.mark.django_db
def test_read_car_models_with_filter_year(user, car_model, create_fifty_car_models):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('car models-list')

    response = client.get(url, {'year': car_model.year})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    car_model_found = False
    for item in results:
        if item['id'] == car_model.id and item["year"] == car_model.year:
            car_model_found = True
            break

    assert car_model_found is True

@pytest.mark.django_db
def test_read_car_models_with_filter_year_gte(user, car_model, create_fifty_car_models):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('car models-list')

    response = client.get(url, {'year_gte': car_model.year})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    assert all(item['year'] >= car_model.year for item in results)

@pytest.mark.django_db
def test_read_car_models_with_filter_year_lte(user, car_model, create_fifty_car_models):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('car models-list')

    response = client.get(url, {'year_lte': car_model.year})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    assert all(item['year'] <= car_model.year for item in results)

@pytest.mark.django_db
def test_read_car_model_id(user, car_model):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('car models-detail', kwargs={'pk': car_model.id})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == car_model.id
    assert response.data["name"] == car_model.name

@pytest.mark.django_db
def test_create_car_model(administrador):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    old_count_car_models = CarModel.objects.count()
    new_car_model = CarModelFactory.stub().__dict__
    
    url = reverse('car models-list')
    response = client.post(url, data=new_car_model)

    new_count_car_models = CarModel.objects.count()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == new_car_model["name"]
    assert new_count_car_models == old_count_car_models + 1

@pytest.mark.django_db
def test_create_car_model_forbidden(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    new_car_model = CarModelFactory.stub().__dict__
    
    url = reverse('car models-list')
    response = client.post(url, data=new_car_model)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_update_car_model(administrador, car_model):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    new_name = "new_name"
    new_manufacturer = "new_manufacturer"
    new_year = 2000 

    car_model.name = new_name
    car_model.manufacturer = new_manufacturer
    car_model.year = new_year

    url = reverse('car models-detail', kwargs={'pk': car_model.id})
    response = client.put(url, data=car_model.__dict__)

    car_model_updated = CarModel.objects.filter(id=car_model.id).first()

    assert response.status_code == status.HTTP_200_OK
    assert car_model_updated.name == new_name
    assert car_model_updated.manufacturer == new_manufacturer
    assert car_model_updated.year == new_year

@pytest.mark.django_db
def test_update_car_model_forbidden(user, car_model):
    access_token = user['access']
    client = APIClient() 
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    car_model.name = "new_name"

    url = reverse('car models-detail', kwargs={'pk': car_model.id})
    response = client.put(url, data=car_model.__dict__)

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_car_model(administrador, car_model):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    old_count_car_models = CarModel.objects.count()
    
    url = reverse('car models-detail', kwargs={'pk': car_model.id})
    response = client.delete(url)

    new_count_car_models = CarModel.objects.count()
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert new_count_car_models == old_count_car_models - 1

@pytest.mark.django_db
def test_delete_car_model_forbidden(user, car_model):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('car models-detail', kwargs={'pk': car_model.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
