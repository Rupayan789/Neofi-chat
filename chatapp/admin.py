from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

user = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'date_joined', 'is_staff')
    list_filter = ('email', 'date_joined', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser','is_online')}),
    )
    add_fieldsets = (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_online', 'is_staff', 'is_superuser'),
        }),


# Register your models here.
admin.site.register(user, CustomUserAdmin)