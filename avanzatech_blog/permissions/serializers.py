from rest_framework import serializers

from avanzatech_blog.permissions.models import Permissions


class PermissionSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Permissions
        fields = ['id', 'name']
        read_only_fields = ['name']
