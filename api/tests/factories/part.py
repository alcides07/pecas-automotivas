import factory
import factory.fuzzy
from faker import Faker
from ...models import Part

faker = Faker()


class PartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Part

    part_number = factory.fuzzy.FuzzyText(length=20)
    name = faker.word()
    details = faker.text(max_nb_chars=255)
    price = factory.fuzzy.FuzzyFloat(low=0, high=9999, precision=2)
    quantity = factory.fuzzy.FuzzyInteger(low=0)
