
from rest_framework import serializers
from django.forms import ValidationError
from categories.models import Categories
from permissions.models import Permissions
from postCategoryPermission.models import postCategoryPermission
from posts.models import Post


# class PostSerializerCreateList(serializers.ModelSerializer):
#     description = serializers.SerializerMethodField

#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'post_content', 'author',
#                   'excerpt', 'created_at', 'public_permission', 'authenticated_permission', 'team_permission', 'author_permission']
#         read_only_fields = ['created_at', 'author']


class PostSerializerCreateList(serializers.ModelSerializer):
    # Define the fields for categories and permissions
    public_permission = serializers.ChoiceField(
        choices=Permissions.objects.values_list('name', flat=True))
    authenticated_permission = serializers.ChoiceField(
        choices=Permissions.objects.values_list('name', flat=True))
    team_permission = serializers.ChoiceField(
        choices=Permissions.objects.values_list('name', flat=True))
    author_permission = serializers.ChoiceField(
        choices=Permissions.objects.values_list('name', flat=True))

    class Meta:
        model = Post
        fields = ['id', 'title', 'post_content', 'author', 'excerpt', 'created_at',
                  'public_permission', 'authenticated_permission', 'team_permission', 'author_permission']
        read_only_fields = ['created_at', 'author']

    def create(self, validated_data):
        # Extract permissions from validated_data
        public_permission = validated_data.pop('public_permission')
        authenticated_permission = validated_data.pop(
            'authenticated_permission')
        team_permission = validated_data.pop('team_permission')
        author_permission = validated_data.pop('author_permission')

        # Create the post
        post = Post.objects.create(**validated_data)

        # Get or create Permissions instances for the provided permissions
        permissions = Permissions.objects.filter(name__in=[
                                                 public_permission, authenticated_permission, team_permission, author_permission])

        # Get or create Categories instances for the fixed categories
        categories = Categories.objects.filter(
            name__in=['public', 'authenticated', 'team', 'author'])

        # Create postCategoryPermission instances
        for category in categories:
            permission = permissions.filter(name=category.name).first()
            if permission:
                postCategoryPermission.objects.create(
                    post_id=post, category_id=category, permission_id=permission)

        return post



class PostSerializerRetrieveUpdateDestroy(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Post
        fields = ['id', 'title', 'post_content', 'author', 'excerpt',
                  'created_at']
        read_only_fields = ['created_at', 'author']
