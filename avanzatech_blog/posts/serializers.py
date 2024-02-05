
from rest_framework import serializers
from django.forms import ValidationError
from posts.models import Post


class PostSerializerCreateList(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Post
        fields = ['id', 'title', 'post_content', 'author',
                  'permission', 'created_at']
        read_only_fields = ['created_at']


class PostSerializerRetrieveUpdateDestroy(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Post
        fields = ['id', 'title', 'post_content', 'author',
                  'permission', 'created_at']
        read_only_fields = ['created_at', 'author']
