from distutils import log
import email
import imp
import re
import os
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
# from .models import 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date
import uuid
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.template import RequestContext
from rest_framework.response import Response
from django.utils.html import strip_tags
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
# from .forms import 
from PIL import Image
from pathlib import Path
import requests
import json
import socket
import platform
from django.utils import timezone



# general variable is declear here
BASE_DIR = Path(__file__).resolve().parent.parent
date = datetime.datetime.today()
year = date.strftime("%Y")
cur_date = datetime.datetime.now()
current_now = timezone.now()
client_ip_address = socket.gethostbyname(socket.gethostname())
device_name = socket.gethostname()
sms_notify = 1
email_notify = 1

paystack_sk = 'Bearer '
paystack_pk = ''

general_list = {
    'site_dev':"Ethion-Tech",
    'dev_link':'https://ethiontech.com',
    'site_name':"Kotel",
    'site_url':"",
    'site_domain':"",
    'currency_symbol':"&#8358;",
    'site_address':"No 1",
    # 'date':date,
    'facebook_link': "#",
    'twitter_link':"#",
    'instagram_link': "#",
    'phone_no':'2348145264707',
    'email':'christaiwo@ethiontech.com',
    'client_ip_address':client_ip_address,
    'device_name':device_name,
    'paystack_sk':paystack_sk,
    'paystack_pk':paystack_pk,
    'year':year,

}


def test(request):
    # active_tradings = tradings.objects.filter(status=1)

    # # loop through the trading and reward users 
    # for trading in active_tradings:
    #     if trading.next_day == date :
    #         if trading.duration == trading.active_days:
    #             tradings.objects.filter(id=trading.id).update(status=0)
    #         else:
    #             user = User.objects.get(id=trading.user_id)
    #             Profile.objects.filter(user_id=trading.user_id).update(balance=float(user.profile.balance) + float(trading.daily_profit) )

    #             tradings.objects.filter(id=trading.id).update(active_days=trading.active_days + 1)

    #             earning_insert = earnings(amount=trading.daily_profit, date=date, tradings_id=trading.id, user_id=trading.user_id)
                #earning_insert.save()

    return render(request, 'test.html')


def home(request):
    trading_plans = trading_plan.objects.all()
    content = {
        'general_list':general_list,
        'page_name': "Home",
        'trading_plans': trading_plans
    }
    return render(request, 'index.html', content)


# for user registeration
def account_register(request):
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Register',

    }
    if request.user.is_authenticated:
        return redirect('account')
    # check for the form request
    elif request.method == 'POST' and request.POST.get('register') == 'register':            
        email = request.POST.get('email')
        username = request.POST.get('username').lower()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # check if user already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('account_register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exist')
            return redirect('account_register')
        else:
            # create user 
            user = User.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.profile.phone_no = phone_no 
            user.profile.address = address 
            user.save()

            # authenticate user and log them in
            login(request, user)

            return redirect('account')

    return render(request, 'account/register.html', context)

# for user login
def account_login(request):
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',

    }

    if request.user.is_authenticated:
        return redirect('account')
    # get the login form 
    elif request.method == 'POST' and request.POST.get('login') == 'login':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if 'next' in request.GET:
                next_url = request.GET['next']
                return redirect('..'+next_url)
            else:
                return redirect('account')
        else:
            messages.error(request, 'Username OR password is incorrect')
            return redirect('account_login')

    return render(request, 'account/login.html', context)

# for user log out
def account_logout(request):
    logout(request)
    return redirect('account_login')


# for user account
@login_required(login_url=account_login)
def account(request):
    user = User.objects.get(username=request.user)
    total_deposit = deposit.objects.filter(user_id=user.id, status=1).aggregate(Sum('amount'))
    total_withdraw = withdraw.objects.filter(user_id=user.id, status=1).aggregate(Sum('amount'))
    total_invest = tradings.objects.filter(user_id=user.id, status=1).aggregate(Sum('amount'))
    total_earning = earnings.objects.filter(user_id=user.id).aggregate(Sum('amount'))
    
    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User account',
        'user':user,
        'total_deposit':total_deposit,
        'total_withdraw':total_withdraw,
        'total_invest':total_invest,
        'total_earning':total_earning,
    }
    return render(request, 'account/index.html', context)


# payment views is declear here
@login_required(login_url=account_login)
def account_profile(request):
    user = User.objects.get(username=request.user)
    
    # redirect if user is not activated
    if user.profile.status == 0:
        return redirect('verification')
    
    # get the submited post
    if request.method == 'POST':
        if request.POST.get('submit') == 'update':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_no = request.POST.get('phone_no')

            User.objects.filter(username=user.username).update(first_name=first_name, last_name=last_name)
            Profile.objects.filter(user_id=user.id).update(phone_no=phone_no)

            # user_update.update()
            messages.success(request, 'UPDATED')
            return redirect('account_profile')
        elif request.POST.get('submit') == "change_password":
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            user_auth = authenticate(username=user.username, password=password)
            if user_auth is not None:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, 'UPDATED')
                return redirect('account_profile')
            else:
                messages.error(request, 'Password incorect')
                return redirect('account_profile')


    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Profile',
        'user':user,
    }
    return render(request, 'account/profile.html', context)


# payment views is declear here
@login_required(login_url=account_login)
def account_deposit(request):
    user = User.objects.get(username=request.user)
    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Deposit',
        'user':user,
    }
    
    if user.profile.status == 0:
        return redirect('verification')
    return render(request, 'account/deposit.html', context)


# user deposit check
@login_required(login_url=account_login)
def account_deposit_check(request, pk):
    user = User.objects.get(username=request.user)
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Deposit',
        'user':user,
    }

    url = "https://api.paystack.co/transaction/verify/"+pk
    headers = {
        'Authorization': paystack_sk,
        'Cache-Control': 'no-cache',
    }

    # get the result and convert it to a json file
    result=requests.get(url,headers=headers)
    result = result.json()
    main_status = result['status']

    if main_status == True:
        amount = result['data']['amount']
        amount = float(amount) / 100;
        status = result['data']['status']

        # check if the transaction is success
        if status == 'success':
            # check if the transaction is in database
            check_ref = deposit.objects.filter(reference_id=pk).count()
            if check_ref == 0:
                # insert into the database
                trx_id = uuid.uuid4().hex[:10]
                str(trx_id)
                deposit_insert = deposit(user_id=user.id, trx_id=trx_id, reference_id=pk, amount=amount, method='paystack', date=date, status=1)
                deposit_insert.save()
                # update user balance
                new_balance = float(user.profile.balance) + float(amount)
                Profile.objects.filter(user_id=user.id).update(balance=new_balance)

                messages.success(request, 'deposit successfully')
            else:
                return redirect('account_deposit')

    return redirect('account_deposit')


# payment views is declear here
@login_required(login_url=account_login)
def account_withdraw(request):
    user = User.objects.get(username=request.user)

    # rediect if user is not active
    if user.profile.status == 0:
        return redirect('verification')

    # check for submited post
    if request.method == 'POST' and request.POST.get('submit') == 'withdraw':
        amount = request.POST.get('amount')

        # check if amount is greater than the withdraw amount and amount is not less than zero
        if float(amount) > float(user.profile.balance) or float(amount) <= 0:
            messages.error(request, 'Insufficient fund')
            return redirect('account_withdraw')
        else:
            # insert withdraw into the database, redirect and show success message
            trx_id = uuid.uuid4().hex[:10].upper()
            withdraw_insert = withdraw(trx_id=trx_id, amount=amount, date=date, status=0, user_id=user.id)
            withdraw_insert.save()
            
            messages.success(request, 'Withdraw request sent pending confirmation')
            return redirect('account_withdraw')

    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Deposit',
        'user':user,
    }
    return render(request, 'account/withdraw.html', context)


# pricing is declear here 
@login_required(login_url=account_login)
def account_pricing(request):
    user = User.objects.get(username=request.user)

    trading_plans = trading_plan.objects.all()
    content = {
        'user': user,
        'general_list':general_list,
        'page_name': "Trading Plan",
        'trading_plans': trading_plans
    }
    if user.profile.status == 0:
        return redirect('verification')

    return render(request, 'account/pricing.html', content)


# def for audit 
@login_required(login_url='../signin')
def account_audit(request, pk):
    user = User.objects.get(username=request.user)
    plan = trading_plan.objects.get(id=pk)
    
    # check for the submited form
    if user.profile.status == 0:
        return redirect('verification')
    
    # get the form input and process it 
    if request.method == "POST":
        if request.POST.get('submit') == "confirm":
            amount = request.POST.get('amount')

            # check if user as money
            if float(user.profile.balance) < float(amount):
                messages.error(request, 'INSUFFICIENT FUND')
                return redirect('account_audit', pk=pk)
            
            elif float(amount) < float(plan.minimum):
                messages.error(request, 'MINIMUM AMOUNT IS $'+plan.minimum )
                return redirect('account_audit', pk=pk)

            elif float(amount) > float(plan.maximum):
                messages.error(request, 'MAXIMUM AMOUNT IS $'+plan.maximum )
                return redirect('account_audit', pk=pk)

            else:
                daily_profit = (float(plan.daily_profit) / 100) * float(amount)
                net_profit = float(daily_profit) * float(plan.duration)
                next_day = datetime.datetime.now() + datetime.timedelta(days=1)
                end = datetime.datetime.now() + datetime.timedelta(days=int(plan.duration))
                tradings_insert = tradings(user_id=user.id, trading_plan_id=plan.id, amount=amount, daily_profit=daily_profit, net_profit=net_profit, duration=plan.duration, active_days=0, next_day=next_day, end=end, withdraw_type=plan.withdraw_type, status=1)
                tradings_insert.save()
                
                # declear the user remaining balance 
                new_balance = float(user.profile.balance) - float(amount) 
                Profile.objects.filter(user_id=user.id).update(balance=new_balance)

                # trouble shoot
                return redirect('account_investment')

    context = {
        'plan':plan,
        'user':user,
        'general_list':general_list,
    }

    return render(request, 'account/audit.html', context)


# for account investment
@login_required(login_url=account_login)
def account_investment(request):
    user = User.objects.get(username=request.user)
    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User account',
        'user':user,
    }
    return render(request, 'account/investments.html', context)


# for user bank investment
@login_required(login_url=account_login)
def account_bank(request):
    user = User.objects.get(username=request.user)
    get_bank = bank.objects.get(user_id=user.id)
    form = bankForm(instance=get_bank)


    # check for post and form is valid
    if request.method == 'POST':
        form = bankForm(request.POST, instance=get_bank)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 1
            obj.save()

            messages.success(request, 'BANK UPDATED')
            return redirect('account_bank')


    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Bank',
        'user':user,
        'form':form,
    }
    return render(request, 'account/bank.html', context)







