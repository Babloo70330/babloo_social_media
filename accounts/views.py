from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm, ProfileEditForm
from .models import Profile


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
        return form


class UserLogoutView(LogoutView):
    pass


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('posts:feed')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)

    from friends.models import Friendship, FriendRequest
    is_self = profile_user == request.user
    is_friend = False
    request_sent = False
    request_received = None
    if not is_self:
        is_friend = Friendship.is_friend(request.user, profile_user)
        request_sent = FriendRequest.objects.filter(
            from_user=request.user, to_user=profile_user, status='pending'
        ).exists()
        request_received = FriendRequest.objects.filter(
            from_user=profile_user, to_user=request.user, status='pending'
        ).first()

    posts = profile_user.posts.all().order_by('-created_at')
    friend_count = Friendship.friend_count(profile_user)

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'is_self': is_self,
        'is_friend': is_friend,
        'request_sent': request_sent,
        'request_received': request_received,
        'posts': posts,
        'friend_count': friend_count,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})
