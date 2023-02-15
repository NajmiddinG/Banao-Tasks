from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import User, Categories, Blog
import os

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
                        # messages.success(request, f"Hello {user}")
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
    orderbylist = ['category', '-date']
    if request.user.type=="D":
        context = {
            "posts": Blog.objects.filter(drafted=False).order_by(*orderbylist) |Blog.objects.filter(drafted=True).order_by(*orderbylist)
        }
    else:
        context = {
            "posts": Blog.objects.filter(drafted=False).order_by(*orderbylist)
        }
    return render(request, "Dashboard.html", context=context)

def create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.type!="D": return redirect('dashboard')
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        category = data.get('category')
        summary = data.get('summary')
        content = data.get('content')
        drafted = 'drafted' in  data.keys()
        if len(request.FILES)==0:
            image = None
        else:
            _, file = request.FILES.popitem()
            image = file[0]
        try:
            Blog.objects.create(created=User.objects.get(id=request.user.id), title=title, image=image, category=Categories.objects.get(id=category), 
                                      summary=summary, content=content, drafted=drafted)
            messages.success(request, f"{title} post created")
            return redirect('dashboard')
        except:
            messages.error(request, "Something is wrong!")
            return redirect('create')
    context = {
        'categories': Categories.objects.all().order_by('-date')
    }
    return render(request, 'create.html', context=context)

def edit(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.type!="D": return redirect('dashboard')
    try:
        if request.user == Blog.objects.get(id=id).created:
            if request.method == "POST":
                data = request.POST
                title = data.get('title')
                category = data.get('category')
                summary = data.get('summary')
                content = data.get('content')
                drafted = 'drafted' in  data.keys()
                if len(request.FILES)==0:
                    Blog.objects.filter(id=id).update(created=User.objects.get(id=request.user.id), title=title, category=Categories.objects.get(id=category), 
                                            summary=summary, content=content, drafted=drafted)
                    messages.success(request, f"{title} post edited")
                    return redirect('dashboard')
                else:
                    image = request.FILES['image']
                    a = Blog.objects.get(id=id)
                    os.remove(a.image.path)
                    Blog.objects.get(id=id).delete()
                    try:
                        Blog.objects.create(created=User.objects.get(id=request.user.id), title=title, image=image, category=Categories.objects.get(id=category), 
                                                summary=summary, content=content, drafted=drafted)
                        messages.success(request, f"{title} post edited")
                        return redirect('dashboard')
                    except:
                        messages.error(request, "Somethingbbjhbhbhb is wrong!")
                        return redirect('dashboard')
            a = Blog.objects.get(id=id)
            context = {
                'data': a,
                'categories': Categories.objects.all().order_by('-date'),
            }
            return render(request, 'edit.html', context=context)
    except:
        messages.error(request, "Something is wrong!")
        return redirect('dashboard')
    

def delete(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.type!="D": return redirect('dashboard')
    try:
        if request.user == Blog.objects.get(id=id).created:
            a = Blog.objects.get(id=id)
            os.remove(a.image.path)
            Blog.objects.get(id=id).delete()
            messages.success(request, f"{a.title} post deleted")
            return redirect('dashboard')
        else:
            messages.error(request, "Something is wrong!")
            return redirect('dashboard')
    except:
        messages.error(request, "Something is wrong!")
        return redirect('dashboard')

def logout(request):
    auth_logout(request)
    return redirect('login')
