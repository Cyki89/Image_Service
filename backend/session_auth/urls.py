from django.urls import path

from . import views

urlpatterns = [
    path('csrf/', views.get_csrf, name='auth-csrf'),
    path('login/', views.LoginView.as_view(), name='auth-login'),
    path('logout/', views.logout_view, name='auth-logout'),
    path('authentication/', views.get_user_if_authenticated, name='auth-session'),
    path('register/', views.RegisterView.as_view(), name='auth-register'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='auth-profile'),
]