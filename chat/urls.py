from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('with/<str:username>/', views.conversation_view, name='conversation'),
    path('poll/<str:username>/', views.poll_messages, name='poll'),
]
