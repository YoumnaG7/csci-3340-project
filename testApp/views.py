from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import FriendRequest
from django.db.models import Q

# Create your views here.

User = get_user_model()

@login_required
def search_users(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.none()

    if query:
        users = User.objects.exclude(
            id=request.user.id
        ).filter(
            username__icontains=query
        ).order_by("username")[:20]

    return render(request, "testApp/friend_search.html", {
        "query": query,
        "users": users,
    })

@login_required
@require_POST
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if receiver == request.user:
        messages.error(request, "You cannot send a friend request to yourself.")

    elif FriendRequest.objects.filter(
        sender=request.user,
        receiver=receiver,
        status=FriendRequest.ACCEPTED
    ).exists() or FriendRequest.objects.filter(
        sender=receiver,
        receiver=request.user,
        status=FriendRequest.ACCEPTED
    ).exists():
        messages.info(request, "You are already friends.")

    elif FriendRequest.objects.filter(
        sender=receiver,
        receiver=request.user,
        status=FriendRequest.PENDING
    ).exists():
        messages.info(request, "This user has already sent you a friend reauest.")

    elif FriendRequest.objects.filter(
        sender=request.user,
        receiver=receiver,
        status=FriendRequest.PENDING
    ).exists():
        messages.info(request, "You already sent this user a friend request.")

    else:
        FriendRequest.objects.create(
            sender=request.user,
            receiver=receiver
        )
        messages.success(request, "Friend request sent!")

    return redirect("search_users")

@login_required
def incoming_requests(request):
    requests = FriendRequest.objects.filter(
        receiver=request.user,
        status=FriendRequest.PENDING
    ).select_related("sender").order_by("-created_at")

    return render(request, "testApp/incoming_requests.html", {
        "requests": requests
    })

@login_required
@require_POST
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status=FriendRequest.PENDING
    )

    friend_request.status = FriendRequest.ACCEPTED
    friend_request.save()

    messages.success(request, "Friend request accepted!")

    return redirect("incoming_requests")

@login_required
def friends_list(request):
    friendships = FriendRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        status=FriendRequest.ACCEPTED
    ).select_related("sender", "receiver")

    friends = []

    for friendship in friendships:
        if friendship.sender_id == request.user.id:
            friends.append(friendship.receiver)
        else:
            friends.append(friendship.sender)

    return render(request, "testApp/friends_list.html", {
        "friends": friends
    })
