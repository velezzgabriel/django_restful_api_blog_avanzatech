
# Register your models here.

from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'post_content', 'author')
    search_fields = ('title', 'post_content')
    # list_filter = ( )
    readonly_fields = ('id',)
    fieldsets = [
        ('Create new post', {'fields': ('title', 'post_content', 'author',)}),]

    # Create a post
    # add_fieldsets = (
    #     ("Create New Post", {
    #         'classes': ('wide',),
    #         'fields': ('title', 'post_content', 'author', 'permission',),
    #     }),
    # )


admin.site.register(Post, PostAdmin)
