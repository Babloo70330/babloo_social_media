from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user2')
    since = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} & {self.user2}"

    @staticmethod
    def is_friend(user_a, user_b):
        return Friendship.objects.filter(
            Q(user1=user_a, user2=user_b) | Q(user1=user_b, user2=user_a)
        ).exists()

    @staticmethod
    def create_friendship(user_a, user_b):
        if user_a.pk > user_b.pk:
            user_a, user_b = user_b, user_a
        return Friendship.objects.get_or_create(user1=user_a, user2=user_b)

    @staticmethod
    def friend_count(user):
        return Friendship.objects.filter(Q(user1=user) | Q(user2=user)).count()

    @staticmethod
    def friends_of(user):
        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        friend_ids = []
        for f in friendships:
            friend_ids.append(f.user2_id if f.user1_id == user.id else f.user1_id)
        return User.objects.filter(id__in=friend_ids)
