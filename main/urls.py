from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('complete/<int:pk>/', views.complete_todo, name='complete_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
]
