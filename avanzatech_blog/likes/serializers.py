from rest_framework import serializers
from likes.models import Like


# class LikeCreateSerializer(serializers.ModelSerializer):
#     description = serializers.SerializerMethodField

#     class Meta:
#         model = Like
#         fields = ['id', 'post_id']
#         read_only_fields = ['created_at', 'modified_at']


class LikeSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Like
        fields = ['id', 'post_id',  'author']
        read_only_fields = ['created_at', 'modified_at']
