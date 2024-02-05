from django.contrib import admin
from .models import Team

# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_name', 'created_at', 'modified_at')
    search_fields = ('team_name',)
    list_filter = ('id',)
    readonly_fields = ('id', 'created_at', 'modified_at')
    fieldsets = [('Team', {'fields': ('team_name',)}),]


admin.site.register(Team, TeamAdmin)
