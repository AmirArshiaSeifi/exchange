from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse as HR
from django.template import loader
from .models import userWallet, price
from decimal import Decimal
import random

def index(request):
    template = loader.get_template('index.html')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        else:
            User.objects.create_user(username=username, password=password)
            userN = User.objects.get(username=username)
            userWallet.objects.create(user_id=userN.id, addr=random.randint(0, 100))
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('wallet')
        else:
            messages.error(request, 'invalid password')
            return redirect('login')
    return render(request, 'login.html')

def wallet(request):
    uW = userWallet.objects.get(user_id=request.user.id)
    p = price.objects.all()[0]
    if request.method == 'POST':
        if "form1" in request.POST:
            charge = float(request.POST['charge'])
            x = request.POST.get('crc')
            setattr(uW, f"{x}_balance", charge)
            uW.save()
            return redirect('wallet')
        elif "form2" in request.POST:
            changeContent = float(request.POST.get('change'))
            currencyNamefrom = request.POST.get('crcf')
            currencyNameto = request.POST.get('crct')
            fromValue = getattr(p, f"{currencyNamefrom}")
            toValue = getattr(p, f"{currencyNameto}")
            if (getattr(uW, f"{currencyNamefrom}_balance")) >= changeContent:
                setattr(uW, f"{currencyNamefrom}_balance", float(getattr(uW, f"{currencyNamefrom}_balance")) - changeContent)
                result = (int(changeContent))*(int(fromValue))/(int(toValue))
                setattr(uW, f"{currencyNameto}_balance", result)
                uW.save()
            return redirect('wallet')
        elif "form3" in request.POST:
            amnt = float(request.POST.get('amount'))
            address =  request.POST.get('address')
            kind = request.POST.get('crcs')
            if (getattr(uW, f"{kind}_balance")) >= amnt:
                des = userWallet.objects.get(addr=address)
                setattr(des, f"{kind}_balance", float(getattr(des, f"{kind}_balance")) + amnt)
                setattr(uW, f"{kind}_balance", float(getattr(uW, f"{kind}_balance")) - amnt)
                des.save()
                uW.save()
            return redirect('wallet')
    return render(request, 'wallet.html', {'uW': uW, 'p': p})