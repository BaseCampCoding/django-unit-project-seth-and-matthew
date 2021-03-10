from django.shortcuts import render
from django.views.generic import UpdateView, TemplateView
from .forms import AnswerForm
from .models import Question
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import random
from users.views import get_possible_questions_id
# Create your views here.

class CongratsView(TemplateView):
    template_name = "completed.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['earned'] = self.request.GET.get("earned")
        return context

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
        congrats = False
        if int(selected_choice) == question.correct_answer:
            streak = request.user.streak
            if request.user.max_challenge_streak == 0:
                if streak > 15:
                    streak = 15
                request.user.points += 10 + ((streak)*5)
                request.user.streak += 1
            else:
                request.user.challenge_streak += 1
                if request.user.challenge_streak == request.user.max_challenge_streak:
                    z = request.user.max_challenge_streak * 100
                    request.user.points += z
                    request.user.challenge_streak = 0
                    request.user.max_challenge_streak = 0
                    congrats = z
        else:
            request.user.streak = 0
            if request.user.max_challenge_streak != 0:
                request.user.challenge_streak = 0
                request.user.max_challenge_streak = 0
        if request.user.streak > request.user.longest_streak:
            request.user.longest_streak = request.user.streak
        badge = check_badge(request.user.points, request.user.streak, str(request.user.badges))
        while badge:
            request.user.badges = str(request.user.badges) + badge
            badge = check_badge(request.user.points, request.user.streak, str(request.user.badges))
        request.user.save()
        if congrats:
            return HttpResponseRedirect("/congrats/?earned="+str(congrats))
        is_random = request.GET.get('random', None)
        if is_random:
            k = "?random=t"
            q_size = Question.objects.count()
            ran = random.randint(1, q_size)
            while ran == question_id:
                ran = random.randint(1,q_size)
        else:
            k = ""
            ran = question_id
            while ran == question_id:
                ran = get_possible_questions_id(question.category)
        return HttpResponseRedirect("/question/" + str(ran) + "/" + k)
        #return HttpResponseRedirect(reverse('question', args=(ran,)))
# list of tuples to store badge data
# (type, value, id)
badge_conditions =[
    (0, 10, '01'),
    (0, 25, '02'),
    (0, 50, '03'),
    (0, 100, '04'),
    (1, 1000, '05'),
    (1, 2500, '06'),
    (1, 5000, '07'),
    (1, 10000, '08'),
    (1, 25000, '09'),
    (1, 50000, '10'),
    (1, 100000, '11'),
]
def check_badge(points, streak, badge_str):
    re_value = None
    for con in badge_conditions:
        if con[0] == 0:
            if streak >= con[1] and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 1:
            if points >= con[1] and not con[2] in badge_str:
                re_value = con[2]
                break
    return re_value