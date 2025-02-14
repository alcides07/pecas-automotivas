import factory
from faker import Faker
from django.contrib.auth.models import User

faker = Faker()


class AdministradorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = faker.user_name()
    email = faker.email()
    password = factory.PostGenerationMethodCall('set_password', faker.password())

    @factory.post_generation
    def set_superuser(self, create, extracted, **kwargs):
        if not create:
            return

        self.is_superuser = True
        self.is_staff = True  
        self.save()

