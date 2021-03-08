from django.shortcuts import render
from django.views.generic import UpdateView, View
from .forms import Answer
from .models import Question
from django.urls import reverse_lazy
# Create your views here.

class AnswerQuestion(UpdateView):
    model = Question
    form = Answer
    fields = []
    template_name = "question.html"
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        instance = Question.objects.get(id=self.request.resolver_match.kwargs["pk"])
        print("WHAT", self.request.POST.get("answer"))
        if self.request.POST.get("answer") == instance.correct_answer:
            print("WOOOOP")
        else:
            print("DEPRESSION")
        return super().form_valid(form)