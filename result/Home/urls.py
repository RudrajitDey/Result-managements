from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    # Expose the manage_course view directly so CRUD redirects
    # can reliably use the `manage_course` URL name.
    path('course/', views.manage_course, name='manage_course'),
    path('student/', views.manage_student, name='manage_student'),
    path('add_result/', views.manage_result, name='manage_result'),
    path('view-result/', views.view_result, name='view_result'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('download/<int:id>/', views.download_result, name='download_result'),
]
