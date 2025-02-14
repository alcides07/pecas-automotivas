import pytest
from .factories import UserFactory, CarModelFactory, PartFactory, AdministradorFactory
from .helpers import login

@pytest.fixture
def car_model():
    return CarModelFactory()

@pytest.fixture
def part():
    return PartFactory()

@pytest.fixture
def user():
    user_factory = UserFactory()
    token = login(user_factory)

    return {
        'access': token['access'],
        'refresh': token['refresh'],
        'user_data': user_factory.__dict__
    }

@pytest.fixture
def administrador():
    administrador_factory = AdministradorFactory()
    token = login(administrador_factory)

    return {
        'access': token['access'],
        'refresh': token['refresh'],
        'administrador_data': administrador_factory.__dict__
    }