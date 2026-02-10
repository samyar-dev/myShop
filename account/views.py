from django.shortcuts import render, redirect
from . forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from cart.SMSservises import verifiction
from . forms import VerifictionPhoneForm
import random
from account.models import ShopUser
from django.http import HttpResponse



# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, phone=request.POST['phone'], password=request.POST['password']
            )
            if user:
                login(request, user)
                return redirect("shop:products")
    form = LoginForm()
    return render(request, "registration/login.html", {'form': form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(
                request, phone=request.POST['phone'], password=request.POST['password']
            )
            login(request, user)
            return redirect("shop:products")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})


def verify_phone(request):
    if not request.user:
        if request.method == 'POST':
            form = VerifictionPhoneForm(data=request.POST)
            if form.is_valid():
                code = ''.join(random.choices('0123456789', k=6))
                request.session['verify_code'] = code
                request.session['phone'] = request.POST['phone']
                verifiction("09937291493", code)
                return redirect('order:verify_code')
        else:
            form = VerifictionPhoneForm()
        return render(request, "orders/verify-phone.html", {'form': form})
    return redirect('order:create_order')


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session['verify_code']:
            if request.user in ShopUser.objects.all():
                user = ShopUser.objects.create_user(phone=request.session['phone'])
                user.save()
            login(request, user)
            if 'verify_code' in request.session:
                del request.session['verify_code']
                del request.session['phone']
                return redirect('order:create_order')
        else:
            return HttpResponse('code verification is not Valid!')
    return render(request, "orders/verify-code.html")