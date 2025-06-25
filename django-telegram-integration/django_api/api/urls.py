from django.urls import path
from .views import get_user_info, register_telegram_user


urlpatterns = [
    path('user-info/', get_user_info, name='user_info'),
    path('register-telegram/', register_telegram_user, name='register_telegram'),
]