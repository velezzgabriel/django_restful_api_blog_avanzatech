from rest_framework import serializers
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'author', 'comment_content', 'created_at'
                  ]
        read_only_fields = ['id', 'created_at']
