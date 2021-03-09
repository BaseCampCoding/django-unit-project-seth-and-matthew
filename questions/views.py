from django.shortcuts import render
from django.views.generic import UpdateView, View
from .forms import AnswerForm
from .models import Question
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import random
# Create your views here.

def AnswerQuestion(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = request.POST['choice']
    except:
        # Redisplay the question voting form.
        return render(request, 'question.html', {
            'question': question,
            'error_message': "Please pick an answer",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        if int(selected_choice) == question.correct_answer:
            streak = request.user.streak
            request.user.points += 10 + ((streak)*5)
            request.user.streak += 1
        else:
            if request.user.streak > request.user.longest_streak:
                request.user.longest_streak = request.user.streak
            request.user.streak = 0
        request.user.save()
        q_size = Question.objects.count()
        ran = random.randint(1, q_size)
        while ran == question_id:
            ran = random.randint(1,q_size)
        return HttpResponseRedirect(reverse('question', args=(ran,)))