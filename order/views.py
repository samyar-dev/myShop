from django.shortcuts import render, redirect, get_object_or_404
from . forms import OrderCreationForm
from account.models import ShopUser
from . models import OrderItem, Order
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from cart.SMSservises import verifiction
from cart.cart import Cart
import random
from django.conf import settings
from django.http import HttpResponse
import requests # type:ignore
import json

# Create your views here.


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            request.session['order_id'] = order.pk
            i = 0
            for order_item in cart:
                order_item = OrderItem.objects.create(product=order_item['product'], order=order, price=order_item['price'],
                                                      quantity=order_item['quantity'], weight=order_item['weight'])
                i += 1
            return redirect('order:send_request')
    else:
        form = OrderCreationForm()
    return render(request, "orders/create-order.html", {'form': form})


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay"

# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = "YOUR_PHONE_NUMBER"  # Optional
# Important: need to edit for real server
CallbackURL = 'http://127.0.0.1:8000/order/verify/'

def send_request(request):
    cart = Cart(request)
    data = {
        'MerchantID': settings.MERCHANT,
        'Amount': cart.get_total_price(),
        'Description': '',
        'Phone': request.user.phone,
        'CallbackURL': CallbackURL
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)),}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                cart.clear()
                return redirect(ZP_API_STARTPAY+authority)
            else:
                print(response_json)
                print(len(settings.MERCHANT))
                return HttpResponse('Error')
        return HttpResponse('response Failed')
    except requests.exceptions.Timeout:
        return HttpResponse('timeout error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')
    

def verify(request):
    order = get_object_or_404(Order, id=request.session.get('order_id'))
    data = {
        'MerchantID': settings.MERCHANT,
        'Amount': order.get_total_price,
        'Authority': request.GET.get('Authority')
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data)),}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']
            if response_json['Status'] == 100:
                order.paid = True
                return HttpResponse(f'successfull , RefID: {reference_id}')
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('timeout error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')
    


def order_detail(request, page_id):
    user = request.user
    if user.has_perm_to_see(page_id):
        orders = Order.objects.filter(Order, buyer=user)
        return render(request, "orders/order-detail.html", {'orders': orders})
    return HttpResponse("you`re not allowed to view!")

# from django.contrib.auth.decorators import permission_required

# @permission_required
# def user_perm(user):
#     return user.orders