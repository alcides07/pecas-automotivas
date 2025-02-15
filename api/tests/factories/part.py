import factory
import factory.fuzzy
from faker import Faker
from ...models import Part

faker = Faker()


class PartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Part

    part_number = factory.fuzzy.FuzzyText(length=20)
    name = factory.fuzzy.FuzzyText(length=10)
    details = faker.text(max_nb_chars=255)
    price = factory.fuzzy.FuzzyDecimal(low=0, high=9999.99, precision=2)
    quantity = factory.fuzzy.FuzzyInteger(low=1, high=9000)

class PartFactoryZeroQuantity(PartFactory):
    quantity = 0