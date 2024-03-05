from rest_framework import serializers

from avanzatech_blog.categories.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Categories
        fields = ['id', 'name']
        read_only_fields = ['name']
