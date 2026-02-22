from django.shortcuts import render, get_object_or_404
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST


# Create your views here.
@require_POST
def add_to_cart(request, pk):
     product = get_object_or_404(Product, id=pk)
     cart = Cart(request)
     cart.add(product)
     context = {
         'total_items': len(cart)
     }
     return JsonResponse(context)


def cart_detail(request):
    return render(request, "cart/cart_detail.html")


@require_POST
def update_quantity(request):
    product_id = request.POST['id']
    product = get_object_or_404(Product, id=product_id)
    action = request.POST['action']
    cart = Cart(request)
    try:
         if action == 'increase':
              cart.add(product)
         else:
              cart.decrease(product)
         return JsonResponse({
              'total_items': len(cart)
         })
    except:
         return JsonResponse({
              'error': 'request is Invalid'
         })
    

def remove_item(request):
    product_id = request.POST.get('itemID')
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse(
         {'total-items': len(cart)}
    )


