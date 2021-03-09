from django.shortcuts import render
from .models import CustomUser
from django.views.generic import CreateView, ListView, DetailView
from .forms import CreateUserForm, ChangeUserForm
from django.urls import reverse_lazy
from questions.models import Question
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
import random

all_categories = ["Python"] # IMPORTANT

# Create your views here.

def get_possible_questions_id(q_category):
    """
    used to generate a question for a given category.
    this function returns the PK of a random question object that fits the question category.
    """
    q_ids = Question.objects.filter(category=q_category).values_list("pk", flat=True)
    print(q_category)
    q_ids = list(q_ids)
    maxi_id = max(q_ids)
    ran = None
    while not ran in q_ids:
        ran = random.randint(1, maxi_id)
    return ran

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
        context["random_number"] = random.randint(1, q_size)
        for cat in all_categories:
            context["cat_" + cat] = get_possible_questions_id(cat)
        return context


class UserProfile(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/user_profile.html"
