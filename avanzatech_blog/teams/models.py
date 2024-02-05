from django.db import models

# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name
