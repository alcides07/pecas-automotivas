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
def test_create_part(part):
    assert part.part_number is not None
    assert part.name is not None
    assert part.details is not None
    assert part.price is not None
    assert part.quantity is not None
    assert Part.objects.count() == 1    

@pytest.mark.django_db
def test_update_part(part):
    old_part = deepcopy(part)

    new_part_number = "new_part_number"
    new_name = "new_name"
    new_details = "new_details"
    new_price = 199.99
    new_quantity = 900

    part.part_number = new_part_number
    part.name = new_name
    part.details = new_details
    part.price = new_price
    part.quantity = new_quantity

    part.save()

    assert part.part_number != old_part.part_number
    assert part.name != old_part.name
    assert part.details != old_part.details
    assert part.price != old_part.price
    assert part.quantity != old_part.quantity

    assert part.part_number == new_part_number
    assert part.name == new_name
    assert part.details == new_details
    assert part.price == new_price
    assert part.quantity == new_quantity

@pytest.mark.django_db
def test_associate_car_model_with_part(part, car_model):
    initial_car_model_count = part.car_models.count()

    part.car_models.add(car_model)
    part.save()

    assert part.car_models.count() == initial_car_model_count + 1

    assert car_model in part.car_models.all()

@pytest.mark.django_db
def test_delete_part(part):
    assert Part.objects.count() == 1

    part.delete()

    assert Part.objects.count() == 0
