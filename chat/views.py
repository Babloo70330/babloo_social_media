from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from .models import Message
from friends.models import Friendship


@login_required
def inbox_view(request):
    threads = Message.inbox_threads(request.user)
    friends = Friendship.friends_of(request.user)
    thread_user_ids = [t['user'].id for t in threads]
    friends_no_thread = [f for f in friends if f.id not in thread_user_ids]
    return render(request, 'chat/inbox.html', {
        'threads': threads,
        'friends_no_thread': friends_no_thread,
    })


@login_required
def conversation_view(request, username):
    other_user = get_object_or_404(User, username=username)

    if not Friendship.is_friend(request.user, other_user):
        messages.error(request, 'You can only chat with your friends.')
        return redirect('chat:inbox')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
        return redirect('chat:conversation', username=username)

    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    thread = Message.conversation(request.user, other_user)
    return render(request, 'chat/conversation.html', {
        'other_user': other_user,
        'thread': thread,
    })


@login_required
def poll_messages(request, username):
    """Returns rendered HTML of the message thread — used for lightweight polling refresh."""
    other_user = get_object_or_404(User, username=username)
    if not Friendship.is_friend(request.user, other_user):
        return JsonResponse({'error': 'not friends'}, status=403)

    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    thread = Message.conversation(request.user, other_user)
    html = render_to_string('chat/_messages.html', {'thread': thread}, request=request)
    return JsonResponse({'html': html, 'count': thread.count()})
