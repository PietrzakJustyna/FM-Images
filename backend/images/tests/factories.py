import factory
from factory.django import DjangoModelFactory


class ImageFactory(DjangoModelFactory):
    title = factory.Faker("city")
    width = 5
    height = 5
    image_file = factory.django.ImageField()

    class Meta:
        model = "images.Image"
