from django.shortcuts import render
from .models import CustomUser
from django.views.generic import CreateView, ListView
from .forms import CreateUserForm, ChangeUserForm
from django.urls import reverse_lazy
from questions.models import Question
import random
# Create your views here.


class SignUpView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"


class HomePageView(ListView):
    template_name = "home.html"
    model = CustomUser
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q_size = Question.objects.count()
        context['random_number'] = random.randint(1,q_size)
        return context