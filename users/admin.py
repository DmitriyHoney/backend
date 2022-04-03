from pyexpat import model
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('pk', 'email', 'get_full_name', 'get_groups', 'is_archive', 'is_superuser', 'avatar')
    list_display_links = ('pk', 'email', 'get_full_name',)
    list_editable = ('is_archive', 'is_superuser',)
    sortable_by = ('pk', 'email', 'is_archive', 'avatar', 'is_superuser')
    search_fields = ('pk', 'email', 'firstname', 'lastname', 'middlename', )
    list_filter = ('is_archive', 'is_superuser', )

    def get_fields(self, obj, req):
        return ['email', 'password', 'lastname', 'firstname', 'middlename', 'avatar', 'groups', 'is_archive', 'is_superuser', ]
    

admin.site.register(User, CustomUserAdmin)