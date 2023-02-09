from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import User

def login(request):
    if request.POST:
        if "signin" in request.POST:
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, f"Hello {username}")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Something is wrong")
            except:
                messages.error(request, "Something is wrong")
        elif "signup" in request.POST:
            try:
                data = request.POST
                if data.get('password1')==data.get('password2'):
                    try:                        
                        if len(request.FILES)==0:
                            picture = None
                        else:
                            _, file = request.FILES.popitem()
                            picture = file[0]
                        
                        user = User.objects.create_user(first_name=data.get('first_name'), last_name=data.get('last_name'),
                                            username=data.get('username'), password=data.get('password1'), picture=picture, email=data.get('email'), address=data.get('address'), type=data.get('type'))
                        auth_login(request, user)
                        messages.success(request, f"Hello {user}")
                        return redirect('dashboard')
                    except:
                        messages.error(request, "Username or Email is exist")
                else:
                    messages.error(request, "Passwords are not similar")
            except:
                messages.error(request, "Something is wrong")
    return render(request, 'Login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "Dashboard.html")

def logout(request):
    auth_logout(request)
    return redirect('login')
