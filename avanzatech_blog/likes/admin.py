# Register your models here.

from django.contrib import admin
from .models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'author', 'created_at',
                    'modified_at')
    search_fields = ()
    list_filter = ()
    readonly_fields = ('id', 'author')
    fieldsets = [
        ('Likes', {'fields': ('author',)}),]


admin.site.register(Like, LikeAdmin)
