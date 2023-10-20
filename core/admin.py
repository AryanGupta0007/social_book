from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email',  'is_active')
    ## These are the fields visible on admin panel
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password', 'profile_photo', 'date_of_birth', 'first_name',
                                         'last_name', 'bio', 'location', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)