from django.shortcuts import render, redirect
from apps.app_login_reg.models import *
import bcrypt
from django.contrib import messages

def index(request):
    request.session.flush()
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else :
        r_user = User.objects.create(first_name = request.POST['fname'], \
            last_name = request.POST['lname'], email = request.POST['email'], \
            password = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()))
        
        request.session['name'] = r_user.first_name
        request.session['id'] = r_user.id
        request.session['registered'] = True
    return redirect('/success')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for tag, error in login_errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        l_user = User.objects.get(email=request.POST['email'])
        request.session['name'] = l_user.first_name
        request.session['id'] = l_user.id
        request.session['logged_in'] = True  
    return redirect('/success')

def success(request):
    if 'id' in request.session:
        return render(request, "success.html")
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')