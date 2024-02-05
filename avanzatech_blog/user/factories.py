# factories.py
import factory
from .models import CustomUser
from teams.factories import TeamFactory, TeamFactorySameTeam
from factory.django import DjangoModelFactory

# class TeamFactory(factory.Factory):
#     class Meta:
#         model = CustomUser

#     team_id = factory.Faker('word')


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    """
    Override the default _create method to use create_user.
    """
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    team_id = factory.SubFactory(TeamFactory)


# class CustomUserSameTeamFactory(DjangoModelFactory):
#     class Meta:
#         model = CustomUser

#     """
#     Override the default _create method to use create_user.
#     """
#     @classmethod
#     def _create(cls, model_class, *args, **kwargs):
#         """Create an instance of the model, and save it to the database."""
#         if cls._meta.django_get_or_create:
#             return cls._get_or_create(model_class, *args, **kwargs)

#         manager = cls._get_manager(model_class)
#         return manager.create_user(*args, **kwargs)

#     username = factory.Faker('user_name')
#     email = factory.Faker('email')
#     password = factory.Faker('password')
#     team_id = factory.SubFactory(TeamFactory)
