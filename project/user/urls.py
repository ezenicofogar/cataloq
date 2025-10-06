from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
]
