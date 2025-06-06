from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history, name='history'),
    path('information/', views.information, name='information'),
    path('profile/', views.profile, name='profile'),
]
