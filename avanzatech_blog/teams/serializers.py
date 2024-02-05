from rest_framework import serializers
from teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField

    class Meta:
        model = Team
        fields = ['id', 'team_name']
