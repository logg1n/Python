from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IndexView, ProfileView, RegisterView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]