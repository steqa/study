from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:pk>/', views.room, name='room'),
    path('create-room/', views.room_create, name='room-create'),
    path('update-room/<int:pk>/', views.room_update, name='room-update'),
    path('delete-room/<int:pk>/', views.room_delete, name='room-delete'),
    path('delete-message/<int:pk>/', views.message_delete, name='message-delete'),

    path('sign-up/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]