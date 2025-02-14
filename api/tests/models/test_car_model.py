import pytest
from ...models import CarModel, Part
from ..factories import CarModelFactory, PartFactory
from copy import deepcopy

@pytest.fixture
def car_model():
    return CarModelFactory()

@pytest.fixture
def part():
    return PartFactory()

@pytest.mark.django_db
def test_create_car_model(car_model):
    assert car_model.name is not None
    assert car_model.year is not None
    assert car_model.manufacturer is not None
    assert CarModel.objects.count() == 1

    assert car_model.parts.count() >= 1  
    
    part = car_model.parts.first()
    assert part is not None
    assert isinstance(part, Part)

@pytest.mark.django_db
def test_update_car_model(car_model):
    old_car_model = deepcopy(car_model)

    new_name = "new_name"
    new_year = "2015"
    new_manufacturer = "new_manufacturer"

    car_model.name = new_name
    car_model.year = new_year
    car_model.manufacturer = new_manufacturer

    car_model.save()

    assert car_model.name != old_car_model.name
    assert car_model.year != old_car_model.year
    assert car_model.manufacturer != old_car_model.manufacturer

    assert car_model.name == new_name
    assert car_model.year == new_year
    assert car_model.manufacturer == new_manufacturer

@pytest.mark.django_db
def test_associate_part_with_car_model(car_model, part):
    initial_part_count = car_model.parts.count()

    car_model.parts.add(part)
    car_model.save()

    assert car_model.parts.count() == initial_part_count + 1

    assert part in car_model.parts.all()

@pytest.mark.django_db
def test_delete_car_model(car_model):
    assert CarModel.objects.count() == 1

    car_model.delete()

    assert CarModel.objects.count() == 0
