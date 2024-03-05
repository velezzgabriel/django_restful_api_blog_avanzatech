from django.db import models

from posts.models import Post
from categories.models import Categories
from permissions.models import Permissions

# Create your models here.


class postCategoryPermission(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    permission_id = models.ForeignKey(Permissions, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pivoting post: {self.post_id} with category: {self.category_id} and permission: {self.permission_id}"