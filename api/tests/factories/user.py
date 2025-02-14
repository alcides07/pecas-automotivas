import factory
from faker import Faker
from django.contrib.auth.models import User

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = faker.user_name()
    email = faker.email()
    password = factory.PostGenerationMethodCall('set_password', '123')
