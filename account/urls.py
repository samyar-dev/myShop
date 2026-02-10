from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('verify-code/', views.verify_code, name='verify_code'),
    # path('register/', views.register, name="register"),
]