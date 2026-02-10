from django.shortcuts import render, get_object_or_404
from . models import Category, Product
from . forms import SearchForm
from cart.cart import Cart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
# import json

# Create your views here.

# partials
def partials(request, name):
    return render(request, f"partials/{name}.html/")


def products(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = categories.get(slug=category_slug)
        products = products.filter(category=category)
    
    context = {'categories': categories, 'products': products}
    return render(request, "shop/products.html", context)


def product(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    context = {
        'product': product
    }
    return render(request, "shop/product.html", context)


@require_POST
def like_view(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user in product.liked_by.all():
        product.liked_by.remove(request.user)
        liked = False
    else:
        product.liked_by.add(request.user)
        liked = True

    response_data = {'liked': liked}
    return JsonResponse(response_data)
