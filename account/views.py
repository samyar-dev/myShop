from django.shortcuts import render, redirect
from . forms import RegisterForm
from django.contrib.auth import login, logout
from cart.SMSservises import verification
from . forms import VerifictionPhoneForm
from django.contrib.auth.decorators import login_required
import random
from account.models import ShopUser
from django.http import HttpResponse, JsonResponse



# Create your views here.

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(
#                 request, phone=request.POST['phone'], password=request.POST['password']
#             )
#             login(request, user)
#             return redirect("shop:products")
#     form = LoginForm()
#     return render(request, "registration/login.html", {'form': form})


@login_required
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("shop:products")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = VerifictionPhoneForm(data=request.POST)
        if form.is_valid():
            code = ''.join(random.choices('0123456789', k=6))
            request.session['verify_code'] = code
            request.session['phone'] = request.POST.get('phone')
            verification(request.session.get('phone'), code)
            return redirect('account:verify_code')
    else:
        form = VerifictionPhoneForm()
    return render(request, "registration/verify-phone.html", {'form': form})


def verify_code(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print('xml-request')
        request.session.pop('verify_code', None)
        request.session.pop('phone', None)
        return JsonResponse({'res': 'مهلت شما به پایان رسید لطفا بار دیگر شماره خود را وارد کنید'})
    
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session['verify_code']:
            user = ShopUser.objects.create_user(phone=request.session['phone'])
            user.save()
            login(request, user)
            request.session.pop('verify_code', None)
            request.session.pop('phone', None)
            return redirect('order:create_order')
        else:
            return HttpResponse('hi')
    return render(request, "registration/verify-code.html")


def user_logout(request):
    logout(request)
    return HttpResponse('شما خارج شدید!')