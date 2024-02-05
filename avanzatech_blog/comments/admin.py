from django.contrib import admin

# Register your models here.

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'author', 'comment_content', 'created_at')
    search_fields = ()
    list_filter = ()
    readonly_fields = ('id', 'author')
    fieldsets = [
        ('Comments', {'fields': ('author',)}),]


admin.site.register(Comment, CommentAdmin)
