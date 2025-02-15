import pytest
import json
from django.urls import reverse
from decimal import Decimal
from api.models import Part
from ..helpers import validated_pagination
from rest_framework.test import APIClient
from rest_framework import status
from api.tests.factories import PartFactory
from django.test import override_settings

@pytest.fixture
def create_fifty_parts():
    for _ in range(50):
       PartFactory()

@pytest.mark.django_db
def test_read_parts(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('parts-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_validate_pagination_parts(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('parts-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    
    try:
        assert validated_pagination(response.data) is True
    except (ValueError, KeyError) as e:
        pytest.fail(f"Erro na paginação: {e}")

@pytest.mark.django_db
def test_read_parts_with_filter_name(user, part, create_fifty_parts):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('parts-list')

    short_part_name = part.name[:5]
    response = client.get(url, {'name': short_part_name})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    part_found = False
    for item in results:
        if item['id'] == part.id and item['name'].lower() == part.name.lower():
            part_found = True
            break

    assert part_found is True

@pytest.mark.django_db
def test_read_parts_with_filter_price_gte(user, part, create_fifty_parts):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('parts-list')

    response = client.get(url, {'price_gte': str(part.price)})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    assert all(Decimal(item['price']) >= part.price for item in results)

@pytest.mark.django_db
def test_read_parts_with_filter_price_lte(user, part, create_fifty_parts):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    url = reverse('parts-list')

    response = client.get(url, {'price_lte': str(part.price)})

    assert response.status_code == status.HTTP_200_OK

    results = response.json()["results"]  

    assert all(Decimal(item['price']) <= part.price for item in results)

@pytest.mark.django_db
def test_read_part_id(user, part):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('parts-detail', kwargs={'pk': part.id})
    response = client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == part.id
    assert response.data["name"] == part.name

@pytest.mark.django_db
def test_create_part(administrador):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    old_count_parts = Part.objects.count()
    new_part = PartFactory.stub().__dict__
    
    url = reverse('parts-list')
    response = client.post(url, data=new_part)

    new_count_parts = Part.objects.count()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == new_part["name"]
    assert new_count_parts == old_count_parts + 1

@pytest.mark.django_db
def test_create_part_forbidden(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    new_part = PartFactory.stub().__dict__
    
    url = reverse('parts-list')
    response = client.post(url, data=new_part)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_update_part(administrador, part):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    new_part_number = "new_part_number"
    new_name = "new_name"
    new_details = "new_details"
    new_price = Decimal("199.99")   
    new_quantity = 100

    part.part_number = new_part_number
    part.name = new_name
    part.details = new_details
    part.price = new_price
    part.quantity = new_quantity

    url = reverse('parts-detail', kwargs={'pk': part.id})
    response = client.put(url, data=part.__dict__)

    part_updated = Part.objects.filter(id=part.id).first()

    assert response.status_code == status.HTTP_200_OK
    assert part_updated.part_number == new_part_number
    assert part_updated.name == new_name
    assert part_updated.details == new_details
    assert part_updated.price == new_price
    assert part_updated.quantity == new_quantity

@pytest.mark.django_db
def test_update_part_forbidden(user, part):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    part.part_number = "new_part_number"

    url = reverse('parts-detail', kwargs={'pk': part.id})
    response = client.put(url, data=part.__dict__)

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_part(administrador, part):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    old_count_parts = Part.objects.count()
    
    url = reverse('parts-detail', kwargs={'pk': part.id})
    response = client.delete(url)

    new_count_parts = Part.objects.count()
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert new_count_parts == old_count_parts - 1

@pytest.mark.django_db
def test_delete_part_forbidden(user, part):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('parts-detail', kwargs={'pk': part.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@override_settings(CELERY_TASK_STORE_EAGER_RESULT=True)
@override_settings(CELERY_RESULT_BACKEND='cache+memory://')
def test_upload_parts(administrador):
    access_token = administrador['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    old_count_parts = Part.objects.count()

    url_upload = reverse('parts-parts-upload')

    with open("api/tests/helpers/pecas_automotivas.csv", 'rb') as file_csv:
        response_upload = client.post(url_upload, {'file': file_csv}, format='multipart')

        task_id = response_upload.data["task_id"]

        assert response_upload.status_code == status.HTTP_202_ACCEPTED
        assert task_id != None

        url_check_task_progress = reverse('tasks-list')

        response_task = client.get(url_check_task_progress, {'task_id': task_id})
        assert response_task.status_code == status.HTTP_200_OK
        
        response_task_result = response_task.json()
        response_task_result_dict = json.loads(response_task_result['result'].replace("'", '"'))

        total_linhas_processadas = response_task_result_dict["total_linhas_processadas"]
        total_registros_criados = response_task_result_dict["total_registros_criados"]
        total_registros_atualizados = response_task_result_dict["total_registros_atualizados"]
        message = response_task_result_dict["message"]
        
        new_count_parts = Part.objects.count()

        assert old_count_parts + total_registros_criados == new_count_parts
        assert total_linhas_processadas == total_registros_criados + total_registros_atualizados
        assert message == "CSV importado com sucesso."

@pytest.mark.django_db
def test_upload_parts_forbidden(user):
    access_token = user['access']
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url_upload = reverse('parts-parts-upload')

    with open("api/tests/helpers/pecas_automotivas.csv", 'rb') as file_csv:
        response_upload = client.post(url_upload, {'file': file_csv}, format='multipart')

        assert response_upload.status_code == status.HTTP_403_FORBIDDEN
