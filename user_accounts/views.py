from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msg
from django.views.generic import View
from django.core.paginator import Paginator

from mixins import PermissionRequiredMixin, AdminRequiredMixin, DeleteModelObjectMixin
from .forms import CreateUserAccountForm, AccessRightsForm, UpdateUserAccountForm
from .models import UserAccountsModel
from utils import toggle_user_status, get_user_perms, assert_immutable_user, assert_unmatched_pk


class CreateUserAccount(PermissionRequiredMixin, View):
    perm = 'user_accounts.add_user'

    def get(self, request):
        context = {'form': CreateUserAccountForm(), 'roles': AccessRightsForm()}
        return render(request, 'user_accounts/create_account.html', context)

    def post(self, request):
        form, roles = CreateUserAccountForm(request.POST), AccessRightsForm(request.POST)
        if form.is_valid():
            roles.auth_user = form.instance_user = request.user
            form.save(roles.get_form_data)
            msg.success(request, 'Account created successfully!')
            return redirect('user_accounts:create_user_account')
        msg.error(request, 'There\'s an error in your form, check if username is not taken already')
        return redirect('user_accounts:create_user_account')


class UpdateUserAccount(PermissionRequiredMixin, View):
    perm = 'user_accounts.update_user'
    template = 'user_accounts/update_user_account.html'

    def get(self, request, pk):
        return render(request, self.template, self.get_context(pk))

    def post(self, request, pk):
        assert_unmatched_pk(user_.pk, pk)
        assert_immutable_user(get_object_or_404(UserAccountsModel, pk=pk))
        form, roles = UpdateUserAccountForm(request.POST), AccessRightsForm(request.POST)
        if form.is_valid():
            msg.success(request, 'Account Updated Successfully!')
            roles.auth_user = form.instance_user = request.user
            form.save(pk, roles.get_form_data)
            return redirect('user_accounts:manage_users')
        msg.error(request, 'There is an error in your form!')
        return render(request, self.template, self.get_context(pk))

    def get_context(self, pk) -> dict:
        global user_
        user_ = get_object_or_404(UserAccountsModel, pk=pk)
        assert_immutable_user(user_)
        return {
            'form': UpdateUserAccountForm(instance=user_),
            'roles': AccessRightsForm(data=get_user_perms(user_))
        }


class ManageUserAccount(PermissionRequiredMixin, View):
    perm = 'user_accounts.update_user'

    def get(self, request):
        self.user = request.user
        return render(request, 'user_accounts/manage_users.html', self.get_context)

    @property
    def get_context(self) -> dict:
        users = UserAccountsModel.objects.order_by('username').filter(
            is_admin=False, is_superuser=False, is_immutable=False).exclude(username=self.user.username)
        paginator = Paginator(users, 25)
        page = self.request.GET.get('page')
        paginator_pages = paginator.get_page(page)
        return {
            'paginator_pages': paginator_pages,
        }


class ToggleUserStatus(PermissionRequiredMixin, View):
    perm = 'user_accounts.update_user'

    def post(self, request):
        pk = request.POST['user_id']
        user = get_object_or_404(UserAccountsModel, pk=pk)
        assert_immutable_user(user)
        toggle_user_status(user, request.user)
        return redirect('user_accounts:manage_users')


class DeleteUser(AdminRequiredMixin, DeleteModelObjectMixin, View):
    model = UserAccountsModel
    success_url = 'user_accounts:manage_users'
    values_list = 'username'
