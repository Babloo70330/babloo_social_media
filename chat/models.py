from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:30]}"

    @staticmethod
    def conversation(user_a, user_b):
        return Message.objects.filter(
            Q(sender=user_a, receiver=user_b) | Q(sender=user_b, receiver=user_a)
        ).order_by('created_at')

    @staticmethod
    def inbox_threads(user):
        """Return list of (other_user, last_message, unread_count) for each conversation."""
        msgs = Message.objects.filter(Q(sender=user) | Q(receiver=user)).select_related('sender', 'receiver')
        threads = {}
        for m in msgs:
            other = m.receiver if m.sender_id == user.id else m.sender
            if other.id not in threads or m.created_at > threads[other.id]['last'].created_at:
                threads[other.id] = {'user': other, 'last': m}
        result = []
        for data in threads.values():
            unread = Message.objects.filter(sender=data['user'], receiver=user, is_read=False).count()
            result.append({'user': data['user'], 'last': data['last'], 'unread': unread})
        result.sort(key=lambda x: x['last'].created_at, reverse=True)
        return result
