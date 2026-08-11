from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from friends.models import Friendship


@login_required
def feed_view(request):
    friends = Friendship.friends_of(request.user)
    friend_ids = [u.id for u in friends]
    friend_ids.append(request.user.id)
    posts = Post.objects.filter(user_id__in=friend_ids).select_related('user', 'user__profile')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post published.')
            return redirect('posts:feed')
    else:
        form = PostForm()

    comment_form = CommentForm()
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
    })


@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))
