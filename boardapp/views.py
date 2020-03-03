from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms

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


def good_func(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post.good = post.good + 1
    post.save()
    return redirect('list')


def read_func(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + ' ' +post2
        return redirect('list')


class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title','content','author','images')
    success_url =  reverse_lazy('list')

    def clean_title(self):
        title = self.cleaned_title
        if title is None:
            raise forms.ValidationError("この項目は必須です.")
        return redirect('list')