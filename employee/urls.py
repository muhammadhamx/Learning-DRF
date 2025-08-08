from django.urls import path
from . import views

urlpatterns = [
    path('owner/register/', views.owner_register, name='owner-register'),
    path('login/', views.login, name='login'),
    path('employees/create/', views.employee_create, name='employee-create'),
    path('employees/', views.list_employees, name='employee-list'),
    path('profile/', views.profile, name='profile'),
]
