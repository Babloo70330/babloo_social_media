from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('like/<int:post_id>/', views.like_toggle, name='like_toggle'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
