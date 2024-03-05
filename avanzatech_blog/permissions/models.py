from django.db import models


class Permissions(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return f"Permission name is:  {self.name}"
