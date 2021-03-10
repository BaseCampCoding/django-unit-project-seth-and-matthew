from django.shortcuts import render
from django.views.generic import UpdateView, View
from .forms import AnswerForm
from .models import Question
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import random
from users.views import get_possible_questions_id
# Create your views here.

class CongratsView(View):
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