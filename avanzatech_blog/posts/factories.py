import factory
from .models import Post
from faker import Faker
from user.factories import CustomUserFactory
from factory.django import DjangoModelFactory

fake = Faker()


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = fake.word()
    post_content = fake.text(max_nb_chars=10)
    # Assuming you have a CustomUserFactory
    author = factory.SubFactory(CustomUserFactory)
    permission = factory.Iterator(
        ['public', 'authenticated', 'team', 'author'])
    created_at = fake.date_time_this_decade()
    modified_at = fake.date_time_this_decade()
