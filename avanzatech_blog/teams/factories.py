# factories.py
import factory
from .models import Team
from factory.django import DjangoModelFactory


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team

    team_name = factory.Faker('word')


class TeamFactorySameTeam(DjangoModelFactory):
    class Meta:
        model = Team

    team_name = factory.Faker('word')
