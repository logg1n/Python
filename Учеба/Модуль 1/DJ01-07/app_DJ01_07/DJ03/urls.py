
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='news_home'),
    path('news_add', views.add, name='news_add'),
]