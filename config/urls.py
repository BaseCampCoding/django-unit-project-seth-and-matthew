"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import (
    HomePageView,
    SignUpView,
    UserProfile,
    LeaderboardView,
    ChallengeView,
)
from questions.views import AnswerQuestion, CongratsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomePageView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("question/<int:question_id>/", AnswerQuestion, name="question"),
    path("user/<int:pk>", UserProfile.as_view(), name="user_profile"),
    path("leaderboard/score/", LeaderboardView.as_view(), name="score_board"),
    path("challenge/<int:pk>/", ChallengeView.as_view(), name="challenge"),
    path("congrats/", CongratsView.as_view(), name="congrats"),
    path("friends/", include("friends.urls", namespace="friends")),
]
