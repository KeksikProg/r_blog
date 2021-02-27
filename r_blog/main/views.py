from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Client, FriendRequest, Like


# Friends
@login_required
def send_friend_request(request, userid):
    from_user = request.user
    to_user = Client.objects.get(id=userid)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('Friend request sent')
    else:
        return HttpResponse('friend request was already sent')


@login_required
def accept_friend_request(request, requestid):
    friend_request = get_object_or_404(FriendRequest, id=requestid)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friends request accepted')
    else:
        return HttpResponse('friends request not accepted')


# Likes
def add_like(request, obj):
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type,
        object_id=obj.id,
        user=request.user)
    return like


def remove_like(request, obj):
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.get(
        content_type=obj_type,
        object_id=obj.id,
        user=request.user).delete()


def is_liked(request, obj) -> bool:
    if not request.user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.get(
        content_type=obj_type,
        object_id=obj.id,
        user=request.user)
    return likes.exists()


def get_all_liked(request, obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return Client.objects.filter(
        likes__content_type=obj_type,
        likes__object_id=obj.id)
