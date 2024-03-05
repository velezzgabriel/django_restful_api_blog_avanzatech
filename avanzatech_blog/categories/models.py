from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return f"Category name is:  {self.name}"
