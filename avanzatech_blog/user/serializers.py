from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = CustomUser
        field = ['id', 'username', 'email',
                 'is_staff', 'team_id', 'is_active']  #
