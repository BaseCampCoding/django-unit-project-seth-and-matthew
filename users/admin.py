from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CreateUserForm, ChangeUserForm
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm
    form = ChangeUserForm
    model = CustomUser


UserAdmin.fieldsets += (
    (
        "Custom fields set",
        {"fields": ("points", "streak", "longest_streak", "challenge_streak", "max_challenge_streak", "badges", "completed_problems")},
    ),
)

admin.site.register(CustomUser, CustomUserAdmin)