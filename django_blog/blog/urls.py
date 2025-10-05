
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # Registration and profile
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Login / Logout using Django's auth views (templates live at registration/)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]
