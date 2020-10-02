from django.shortcuts import render, redirect
from django.contrib import messages as msg
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateUserAccountForm, AccessRightsForm


class CreateUserAccount(LoginRequiredMixin, View):
    login_url = 'home:login'

    def get(self, request):
        context = {'form': CreateUserAccountForm(), 'roles': AccessRightsForm()}
        return render(request, 'user_accounts/create_account.html', context)

    def post(self, request):
        form, roles = CreateUserAccountForm(request.POST), AccessRightsForm(request.POST)
        if form.is_valid():
            form.instance_user = request.user
            form.save(roles.get_form_data)
            msg.success(request, 'Account created successfully!')
            return redirect('user_accounts:create_user_account')
        msg.error(request, 'There\'s an error in your form, check if username is not taken already')
        return redirect('user_accounts:create_user_account')
