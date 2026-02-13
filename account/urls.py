from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('phone-login/', views.phone_login, name='phone_login'),
    path('register/', views.register, name="register"),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('logout/', views.user_logout, name='user_logout'),
]