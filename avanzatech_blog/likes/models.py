
from django.db import models
from user.models import CustomUser
from posts.models import Post

# Create your models here.


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Like made by {self.user_id}"
