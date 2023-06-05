import factory
from . import models


class YourModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UserImage

    image = factory.django.ImageField()
