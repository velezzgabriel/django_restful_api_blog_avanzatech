from rest_framework import serializers

from avanzatech_blog.postCategoryPermission.models import postCategoryPermission

class postCategoryPermissionSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = postCategoryPermission
        fields = ['id', 'post_id', 'category_id', 'permission_id']
        read_only_fields = ['post_id', 'category_id']
