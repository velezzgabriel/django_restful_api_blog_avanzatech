import factory
from .models import Like
from faker import Faker
from user.factories import CustomUserFactory
from posts.factories import PostFactory
from factory.django import DjangoModelFactory

fake = Faker()


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    post_id = factory.SubFactory(PostFactory)
    author = factory.SubFactory(CustomUserFactory)
    created_at = fake.date_time_this_decade()
    modified_at = fake.date_time_this_decade()
