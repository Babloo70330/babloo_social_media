from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import FriendRequest, Friendship


@login_required
def send_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if to_user == request.user:
        messages.error(request, "You can't send a friend request to yourself.")
        return redirect('accounts:profile', username=username)

    if Friendship.is_friend(request.user, to_user):
        messages.info(request, 'You are already friends.')
        return redirect('accounts:profile', username=username)

    existing_reverse = FriendRequest.objects.filter(
        from_user=to_user, to_user=request.user, status='pending'
    ).first()
    if existing_reverse:
        return accept_request(request, existing_reverse.id)

    FriendRequest.objects.get_or_create(
        from_user=request.user, to_user=to_user, defaults={'status': 'pending'}
    )
    messages.success(request, f'Friend request sent to {to_user.username}.')
    return redirect('accounts:profile', username=username)


@login_required
def accept_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.status = 'accepted'
    fr.save()
    Friendship.create_friendship(fr.from_user, fr.to_user)
    messages.success(request, f'You are now friends with {fr.from_user.username}.')
    return redirect('friends:requests_list')


@login_required
def reject_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.status = 'rejected'
    fr.save()
    messages.info(request, 'Friend request declined.')
    return redirect('friends:requests_list')


@login_required
def requests_list(request):
    pending = FriendRequest.objects.filter(to_user=request.user, status='pending').select_related('from_user')
    return render(request, 'friends/requests.html', {'pending': pending})


@login_required
def friends_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    friends = Friendship.friends_of(profile_user)
    return render(request, 'friends/list.html', {'profile_user': profile_user, 'friends': friends})


@login_required
def suggestions(request):
    friends = Friendship.friends_of(request.user)
    friend_ids = [u.id for u in friends]
    friend_ids.append(request.user.id)
    sent_ids = FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    suggested = User.objects.exclude(id__in=list(friend_ids) + list(sent_ids)).order_by('-date_joined')[:12]
    return render(request, 'friends/suggestions.html', {'suggested': suggested})
