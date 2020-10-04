from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages as msg
from django.http import Http404

from .forms import LoginForm, ChangePasswordForm
from user_accounts.models import UserAccountsModel


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                msg.success(request, f'Welcome {request.user}')
                return redirect('home:homepage')

            msg.error(request, 'Invalid Credentials!')
            return redirect('home:login')

    return render(request, 'home/login.html', {'login_form': LoginForm()})


def change_password(request):
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            username = change_password_form.cleaned_data['username']
            old_password = change_password_form.cleaned_data['password']
            new_password = change_password_form.cleaned_data['new_password']
            try:
                user = get_object_or_404(UserAccountsModel, username=username)
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()

                    msg.success(request, 'Password Changed Successfully!')
                    return redirect('home:login')

                msg.error(request, 'Password does not match')
                return redirect('home:change_password')
            except Http404:
                msg.error(request, 'Username does not exist')
                return redirect('home:change_password')

        msg.error(request, 'Invalid form data')
        return redirect('home:change_password')

    return render(request, 'home/change_password.html', {'change_form': ChangePasswordForm()})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        msg.success(request, 'Logged Out!')
        return redirect('home:login')


def home(request):
    return render(request, 'home/homepage.html')
