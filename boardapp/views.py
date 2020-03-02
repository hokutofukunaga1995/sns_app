from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def signup_func(request):
    if request.method == "POST":
        username_input = request.POST['username']
        password_input = request.POST['password']
        try:
            User.objects.get(username=username_input)
            return render(request, 'signup.html', {'error':'このユーザーは登録されています'})
        except:
            user = User.objects.create_user(username_input, '', password_input)
            return render(request, 'signup.html', {'some':'somedata'})
    return render(request, 'signup.html', {'some':'somedata'})


def login_func(request):
        if request.method == "POST":
            username_input = request.POST['username']
            password_input = request.POST['password']
            user = authenticate(request, username = username_input, password = password_input)
            if user is not None:
                login(request, user)
                return redirect('signup')
            else:
                return redirect('login')
        return render(request, 'login.html')

    
def list_func(request):
    return render(request, 'list.html')
