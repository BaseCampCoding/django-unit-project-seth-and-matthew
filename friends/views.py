from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
import json
from users.models import CustomUser
from .models import FriendRequest

# Create your views here.


def friend_request_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = user.id
        account = get_object_or_404(CustomUser, pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(
                receiver=account, is_active=True
            )
            context["friend_requests"] = friend_requests
        else:
            return HttpResponse("You can't view another users friend requests.")
    else:
        redirect("login")
    return render(request, "snippets/friend_request.html", context)


def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = CustomUser.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(
                    sender=user, receiver=receiver
                )
                friend_requests.save()
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload["response"] = "Friend request sent."
                except Exception as e:
                    payload["response"] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload["response"] = "Friend request sent"

            if payload["response"] == None:
                payload["response"] = "Something went wrong."
        else:
            payload["response"] = "Unable to send a friend request."
    else:
        payload["response"] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept()
                    payload["response"] = "Friend request accepted."
                else:
                    payload["response"] = "Something went wrong."
            else:
                payload["response"] = "That is not your request to accept."
        else:
            payload["response"] = "Unable to accept that friend request."
    else:
        payload["response"] = "You must be authenticated to accept a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")