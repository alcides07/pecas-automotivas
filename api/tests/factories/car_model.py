import factory
from faker import Faker
from ...models import CarModel
from .part import PartFactory

faker = Faker()

class CarModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarModel

    name = faker.word()
    manufacturer = faker.word()
    year = int(faker.year())

    @factory.post_generation
    def parts(self, create, extracted, **kwargs):
        if not create:
            return

        part = PartFactory()
        self.parts.add(part)
        self.save()
