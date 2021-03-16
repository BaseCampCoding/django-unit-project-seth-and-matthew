from django.shortcuts import redirect, render, HttpResponse
from .models import CustomUser, FriendRequest
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .forms import CreateUserForm, ChangeUserForm
from django.urls import reverse_lazy
from questions.models import Question
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import random

all_categories = [
    "Python",
    "HTML/CSS",
    "Django",
    "Math",
    # "Science",
    # "History",
    # "Video Games",
    # "Movies",
    # "Food",
    # "Sports",
]  # IMPORTANT

# Create your views here.
def get_possible_questions_id(q_category):
    """
    used to generate a question for a given category.
    this function returns the PK of a random question object that fits the question category.
    """
    q_ids = Question.objects.filter(category=q_category).values_list("pk", flat=True)
    q_ids = list(q_ids)
    if q_ids:
        maxi_id = max(q_ids)
    else:
        return 1
    ran = None
    while not ran in q_ids:
        ran = random.randint(1, maxi_id)
    return ran


class ChallengeView(UpdateView):
    model = get_user_model()
    fields = []
    success_url = reverse_lazy("question", args=(random.randint(1, Question.objects.count()-1),))

    def form_valid(self, form):
        form.instance.challenge_streak = 0
        e = int(self.request.GET.get("ch", 5))
        form.instance.max_challenge_streak = e
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
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
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = []
        temp_badge = str(self.object.badges)
        lent = len(temp_badge)
        i = 0
        while i < lent:
            result.append("images/" + temp_badge[i] + temp_badge[i + 1] + ".png")
            i += 2
        context["badge_list"] = result
        temp_list = list()
        int_val = ""
        str_val = ""
        prev = None
        for i in self.object.completed_problems:
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
        context["completed_list"] = temp_list
        return context


class LeaderboardView(ListView):
    model = get_user_model()
    template_name = "leaderboard/top_score.html"

    def get_queryset(self):
        object_list = CustomUser.objects.order_by("-points")[:10]

        return object_list


def SendFriendRequest(request, userID):
    user = request.user
    receiver = CustomUser.objects.get(id=userID)
    friendRequest, created = FriendRequest.objects.get_or_create(
        user=user, receiver=receiver
    )
    if created:
        messages.success(request, "Friend request sent.")
        return redirect(f"/user/{receiver.id}")
    else:
        messages.error(request, "Friend request already created.")
        return redirect(f"/user/{receiver.id}")


def AcceptFriendRequest(request, requestID):
    friendRequest = FriendRequest.objects.get(id=requestID)
    if friendRequest.receiver == request.user:
        friendRequest.user.friends.add(friendRequest.receiver)
        friendRequest.receiver.friends.add(friendRequest.user)
        friendRequest.delete()
        messages.success(request, "Friend request accepted.")
        return redirect(f"/user/{request.user.id}")
    else:
        messages.error(request, "Friend request not accepted.")
        return redirect(f"/user/{request.user.id}")


def DeclineFriendRequest(request, requestID):
    friendRequest = FriendRequest.objects.get(id=requestID)
    if friendRequest.receiver == request.user:
        friendRequest.delete()
        messages.success(request, "Friend request declined.")
        return redirect(f"/user/{request.user.id}")
    else:
        messages.error(request, "Friend request not declined.")
        return redirect(f"/user/{request.user.id}")


def RemoveFriend(request, userID):
    user = request.user
    friend = CustomUser.objects.get(id=userID)
    user.friends.remove(friend)
    friend.friends.remove(user)
    messages.success(request, "Friend removed.")
    return redirect(f"/user/{request.user.id}")
