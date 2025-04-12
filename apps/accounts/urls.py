from django.urls import path
from . import views
from .views import update_profile

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.user_login, name="login"),
    path('accounts/register/', views.register, name="register"),
    path('accounts/logout/', views.user_logout, name="logout"),
    path('searched/', views.searched, name="search"),
    path('accounts/delete/', views.delete_account, name="delete_account"),
    path('update_profile/', update_profile, name='update_profile'),
    path('about/', views.about, name='about'),
]
