from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search_users, name="search_users"),
    path(
        "send-request/<int:user_id>/",
        views.send_friend_request,
        name="send_friend_request"
    ),
    path("requests/", views.incoming_requests, name="incoming_requests"),
    path(
        "accept-request/<int:request_id>/",
        views.accept_friend_request,
        name="accept_friend_request"
    ),
    path("list/", views.friends_list, name="friends_list"),
    path("remove-friend/<int:user_id>/", views.remove_friend, name="remove_friend"),
]