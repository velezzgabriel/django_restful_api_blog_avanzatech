import factory
from .models import Comment
from faker import Faker
from user.factories import CustomUserFactory
from posts.factories import PostFactory
from factory.django import DjangoModelFactory

fake = Faker()


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post_id = factory.SubFactory(PostFactory)
    author = factory.SubFactory(CustomUserFactory)
    comment_content = fake.text()
    created_at = fake.date_time_this_decade()
