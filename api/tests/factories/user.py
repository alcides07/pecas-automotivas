import factory
from faker import Faker
from django.contrib.auth.models import User

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.user_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    password = factory.PostGenerationMethodCall('set_password', '123')
