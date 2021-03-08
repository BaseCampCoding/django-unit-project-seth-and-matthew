from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "points",
            "streak",
            "longest_streak",
        ]


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields