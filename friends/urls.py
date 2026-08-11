from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('send/<str:username>/', views.send_request, name='send_request'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('requests/', views.requests_list, name='requests_list'),
    path('list/<str:username>/', views.friends_list, name='friends_list'),
    path('suggestions/', views.suggestions, name='suggestions'),
]
