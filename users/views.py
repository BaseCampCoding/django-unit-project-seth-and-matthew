from django.shortcuts import render
from .models import CustomUser
from django.views.generic import CreateView

# Create your views here.


class SignUpView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("home")
    template_name = "signup.html"