from django.urls import path

from .views import send_friend_request, friend_request_view, accept_friend_request

app_name = "friends"

urlpatterns = [
    path("friend_request/", send_friend_request, name="friend_request"),
    path("friend_request/<user_id>/", friend_request_view, name="friend_requests"),
    path(
        "accept_friend_request/<friend_request_id>",
        accept_friend_request,
        name="friend_request_accept",
    ),
]