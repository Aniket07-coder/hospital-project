from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctors, name='doctors'),
    path('appointment/', views.appointment, name='appointment'),
    path('success/', views.success, name='success'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('edit-doctor/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('delete-doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('accept-appointment/<int:id>/', views.accept_appointment, name='accept_appointment'),
    path('reject-appointment/<int:id>/', views.reject_appointment, name='reject_appointment'),
    path('my-appointments/', views.user_dashboard, name='user_dashboard'),
    path('admin-appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin-doctors/', views.admin_doctors, name='admin_doctors'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-messages/', views.admin_messages, name='admin_messages'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
]