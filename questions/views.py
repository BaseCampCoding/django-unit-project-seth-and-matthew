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
import json

# Create your views here.

def decompile_answered_questions_str(string) -> list:
    """returns an answered questions string as a list of tuples
    > decomplie_answered_questions_str("4Python3Math")
    [
        (4, "Python"),
        (3, "Math")
    ]
    """
    temp_list = list()
    int_val = ""
    str_val = ""
    prev = None
    for i in string:
        if i.isdigit() and prev and prev.isdigit():
            int_val += i
        elif i.isdigit() and prev and not prev.isdigit():
            temp_list.append(tuple([int(int_val), str_val]))
            int_val = i
            str_val = ""
        elif i.isdigit():
            int_val += i
        else:
            str_val += i
        prev = i
    temp_list.append(tuple([int(int_val), str_val]))
    return temp_list
class CongratsView(TemplateView):
    template_name = "completed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["earned"] = self.request.GET.get("earned")
        return context
class BadgesView(TemplateView):
    template_name = "badges.html"


def AnswerQuestion(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = request.POST["choice"]
    except:
        # Redisplay the question voting form.
        return render(
            request,
            "question.html",
            {
                "question": question,
                "error_message": "Please pick an answer",
            },
        )
    else:
        congrats = False
        if int(selected_choice) == question.correct_answer:
            streak = request.user.streak
            if request.user.max_challenge_streak == 0:
                if streak > 15:
                    streak = 15
                request.user.points += 10 + ((streak) * 5)
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
        if len(request.user.completed_problems) >  0:
            decomp = decompile_answered_questions_str(request.user.completed_problems)
            i = 0
            lent = len(decomp)
            found = False
            while i < lent:
                if decomp[i][1] == question.category:
                    decomp[i] = (str(int(decomp[i][0]) + 1), question.category)
                    found = True
                    break
                i += 1
            if not found:
                decomp.append((1, question.category))
            temp = []
            for i in decomp:
                temp.append(str(i[0]))
                temp.append(i[1]) 
            temp = ''.join(temp)
            # temp_json_save = json.loads(temp)
            # temp = json.dumps(temp_json_save)
            request.user.completed_problems = temp
        else:
            decomp = None
            request.user.completed_problems = '1' + question.category
        
                    
        badge = check_badge(
            request.user.points,
            request.user.streak,
            str(request.user.badges),
            decomp,
        )
        while badge:
            request.user.badges = str(request.user.badges) + badge
            badge = check_badge(
                request.user.points,
                request.user.streak,
                str(request.user.badges),
                decomp,
            )
        request.user.save()
        if congrats:
            return HttpResponseRedirect("/congrats/?earned=" + str(congrats))
        is_random = request.GET.get("random", None)
        if is_random:
            k = "?random=t"
            q_size = Question.objects.count()
            ran = random.randint(1, q_size)
            while ran == question_id:
                ran = random.randint(1, q_size)
        else:
            k = ""
            ran = question_id
            while ran == question_id:
                ran = get_possible_questions_id(question.category)
        return HttpResponseRedirect("/question/" + str(ran) + "/" + k)
        # return HttpResponseRedirect(reverse('question', args=(ran,)))


# list of tuples to store badge data
# (type, value, id)
badge_conditions = [
    (0, 10, "01"),
    (0, 25, "02"),
    (0, 50, "03"),
    (0, 100, "04"),
    (1, 1000, "05"),
    (1, 2500, "06"),
    (1, 5000, "07"),
    (1, 10000, "08"),
    (1, 25000, "09"),
    (1, 50000, "10"),
    (1, 100000, "11"),
    (2, 25, "12"),
    (2, 100, "13"),
    (2, 200, "14"),
    (3, 25, "15"),
    (3, 100, "16"),
    (3, 200, "17"),
    (4, 25, "18"),
    (4, 100, "19"),
    (4, 200, "20"),
    (5, 25, "21"),
    (5, 100, "22"),
    (5, 200, "23"),
    (6, 25, "24"),
    (6, 100, "25"),
    (6, 200, "26"),
    (7, 25, "27"),
    (7, 100, "28"),
    (7, 200, "29"),
    (8, 25, "30"),
    (8, 100, "31"),
    (8, 200, "32"),
    (9, 25, "33"),
    (9, 100, "34"),
    (9, 200, "35"),
    (10, 25, "36"),
    (10, 100, "37"),
    (10, 200, "38"),
]


def check_badge(points, streak, badge_str, completed_list):
    re_value = None
    badge_str = [badge_str[i:i+2] for i in range(0, len(badge_str), 2)]
    for con in badge_conditions:
        if con[0] == 0:
            if streak >= con[1] and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 1:
            if points >= con[1] and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 2 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Python":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 3 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "HTML":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 4 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Django":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break 
        if con[0] == 5 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Math":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break 
        if con[0] == 6 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Science":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break 
        if con[0] == 7 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "History":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 8 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Videogames":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break
        if con[0] == 9 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Movies":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break 
        if con[0] == 10 and completed_list:
            t = None
            for i in completed_list:
                if i[1] == "Food":
                    t = int(i[0])
                    break
            if t and t >= int(con[1]) and not con[2] in badge_str:
                re_value = con[2]
                break 
    return re_value




