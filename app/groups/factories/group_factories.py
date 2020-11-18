import factory

from groups.models import Group


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = "NTNUI Turn"
    description = "We are gymnastics"
    contact_email = factory.Faker("email")
