import factory

from track_and_trace.models import Address, Carrier, Shipment, Product, Article


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = factory.Faker("street_address")
    city = factory.Faker("city")
    zip_code = factory.Faker("postcode")
    country = factory.Faker(
        "random_element",
        elements=["Germany", "France", "Belgium", "Spain", "Netherlands", "Denmark"],
    )


class CarrierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Carrier

    name = factory.Faker("company")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("random_number", digits=2)
    SKU = factory.Faker("bothify", text="??###")


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    article = factory.SubFactory(ProductFactory)
    article_quantity = factory.Faker("random_int", min=1, max=10)


class ShipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shipment

    tracking_number = factory.Faker("bothify", text="??###??###")
    carrier = factory.SubFactory(CarrierFactory)
    sender_address = factory.SubFactory(AddressFactory)
    receiver_address = factory.SubFactory(AddressFactory)
    status = factory.Faker("random_element", elements=Shipment.Status.values)
    articles = factory.RelatedFactoryList(
        ArticleFactory, factory_related_name="shipment"
    )
