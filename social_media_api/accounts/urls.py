from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow'),  # POST to follow, DELETE to unfollow

]
