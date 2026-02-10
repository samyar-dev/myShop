from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('request/', views.send_request, name='send_request'),
    path('verify/', views.verify, name='verify'),
]