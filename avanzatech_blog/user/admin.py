from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'team_id', 'email',
                    'is_active',  'is_staff')
    search_fields = ('username',)
    list_filter = ('is_active',  'is_active', 'team_id', 'is_staff')
    readonly_fields = ('id',)
    fieldsets = (('Personal Info', {'fields': (
        'username', 'team_id', 'email', 'is_active', 'is_staff', 'password')}),)

    # Create a user
    add_fieldsets = (
        ("Create New User", {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'team_id'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
