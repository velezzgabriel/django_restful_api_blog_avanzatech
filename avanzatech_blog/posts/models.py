from django.db import models

# Create your models here.


from user.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    post_content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    excerpt = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.excerpt = self.post_content[:200]
        super(Post, self).save(*args, **kwargs)

        

    def __str__(self):
        return self.title

    # class Meta:
    #     # Orden predeterminado: por fecha de creación ascendente
    #     ordering = ['created_at']
