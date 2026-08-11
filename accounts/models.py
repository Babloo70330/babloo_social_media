from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=250, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_pic = models.ImageField(upload_to='cover_pics/', blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.username})
