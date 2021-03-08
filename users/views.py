from django.shortcuts import render
from .models import CustomUser
from django.views.generic import CreateView, ListView
from .forms import CreateUserForm, ChangeUserForm
from django.urls import reverse_lazy

# Create your views here.


class SignUpView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("home")
    template_name = "signup.html"


class HomePageView(ListView):
    template_name = "home.html"
    model = CustomUser