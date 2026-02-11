from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('partials/<str:name>/', views.partials, name='partials'),
    path('products/', views.products, name='products'),
    path('products/<slug:category_slug>/', views.products, name='products_by_category'),
    path('product/<int:id>/<str:slug>/', views.product, name='product'),
    path('like/<int:id>/', views.like_view, name='like_view'),
    path('search/', views.search, name='search'),
]