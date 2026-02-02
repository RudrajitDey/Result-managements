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
    
    # New beautiful pages
    path('about/', views.about_us, name='about_us'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('achievements/', views.achievements, name='achievements'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('help/', views.help, name='help'),
    path('faqs/', views.faqs, name='faqs'),
    path('help-center/', views.help_center, name='help_center'),
    path('documentation/', views.documentation, name='documentation'),
    path('whatsapp/', views.whatsapp, name='whatsapp'),
    path('status/', views.status, name='status'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
]
