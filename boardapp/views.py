from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import BoardModel

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
                return redirect('list')
            else:
                return redirect('login')
        return render(request, 'login.html')


@login_required
def list_func(request):
    object_list = BoardModel.objects.all()
    if object_list.first() is None:
        return render(request, 'list.html', {'error':'投稿はありません。'})
    return render(request, 'list.html', {'object_list':object_list})

def logout_func(request):
    logout(request)
    return redirect('login')


def detail_func(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})