from django.db import models

# Create your models here.


from user.models import CustomUser


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    post_content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    PERMISSION_CHOICES = [
        ('public', 'non authenticated can read'),
        ('authenticated', 'authenticated can read'),
        ('team', 'team members can read'),
        ('author', 'author can read')
    ]

    permission = models.CharField(
        max_length=15, choices=PERMISSION_CHOICES, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # class Meta:
    #     # Orden predeterminado: por fecha de creación ascendente
    #     ordering = ['created_at']
