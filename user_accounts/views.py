from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msg
from django.views.generic import View
from django.http import Http404
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError

from mixins import (
    PermissionRequiredMixin, DeleteModelObjectMixin, ModuleAccesRedirectMixin,
    ManageModuleViewMixin
)
from .forms import CreateUserAccountForm, CreateRoleForm, UpdateUserAccountForm, UpdateRoleForm
from .models import UserAccountsModel
from utils import toggle_user_status, assert_immutable_user, assert_unmatched_pk, get_group_perms


class MainModuleMixin(ModuleAccesRedirectMixin, View):
    perm_link = (
        ('user_accounts:create_user_account', 'user_accounts.add_user'),
        ('user_accounts:manage_users', 'user_accounts.update_user'),
        ('user_accounts:manage_roles', 'user_accounts.manage_roles')
    )


#############################################
#       USER ACCOUNTS
############################################
class CreateUserAccount(PermissionRequiredMixin, View):
    perm = 'user_accounts.add_user'

    def get(self, request):
        context = {'form': CreateUserAccountForm(), 'roles': Group.objects.all()}
        return render(request, 'user_accounts/create_account.html', context)

    def post(self, request):
        form, role = CreateUserAccountForm(request.POST), request.POST['role']
        if form.is_valid():
            form.instance_user = request.user
            form.save(role=role)
            msg.success(request, 'Account created successfully!')
            return redirect('user_accounts:create_user_account')
        msg.error(request, 'There\'s an error in your form, check if username is not taken already')
        return render(request, 'user_accounts/create_account.html', {'form': form, 'roles': Group.objects.all()})


class UpdateUserAccount(PermissionRequiredMixin, View):
    perm = 'user_accounts.update_user'
    template = 'user_accounts/update_user_account.html'

    def get(self, request, pk):
        return render(request, self.template, self.get_context(pk))

    def post(self, request, pk):
        assert_unmatched_pk(user_.pk, pk)
        assert_immutable_user(get_object_or_404(UserAccountsModel, pk=pk))
        form, role = UpdateUserAccountForm(request.POST), request.POST['role']
        if form.is_valid():
            form.instance_user = request.user
            form.save(pk, role)
            msg.success(request, 'Account Updated Successfully!')
            return redirect('user_accounts:manage_users')
        msg.error(request, 'There is an error in your form!')
        return render(request, self.template, self.get_context(pk))

    def get_context(self, pk: int) -> dict:
        global user_
        user_ = get_object_or_404(UserAccountsModel, pk=pk)
        assert_immutable_user(user_)
        return {
            'form': UpdateUserAccountForm(instance=user_),
            'roles': Group.objects.all(),
            'user_group': user_.groups.all().first()
        }


class ManageUserAccount(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'user_accounts.update_user'
    template = 'user_accounts/manage_users.html'
    values_list_cols = (
        'id', 'username', 'name', 'phone_no', 'gender', 'date_of_birth', 'groups__name', 'date_created',
        'last_login', 'is_active'
    )
    model = UserAccountsModel
    order_col = 'username'
    url_filter_kwargs = (
        ('gender', 'gender'),
        ('role', 'groups__name__icontains'),
        ('search', 'name__icontains')
    )
    extra_context = {'roles': Group.objects.all()}

    @property
    def query_set(self):
        filter_fields = {'is_admin': False, 'is_superuser': False, 'is_immutable': False}
        exclude = {'username': self.request.user.username}
        return super().query_set.filter(**filter_fields).exclude(**exclude)


class ToggleUserStatus(PermissionRequiredMixin, View):
    perm = 'user_accounts.update_user'

    def post(self, request):
        pk = request.POST['user_id']
        user = get_object_or_404(UserAccountsModel, pk=pk)
        assert_immutable_user(user)
        toggle_user_status(user, request.user)
        return redirect('user_accounts:manage_users')


class SetUserPassword(PermissionRequiredMixin, View):
    perm = 'user_accounts.set_password'

    def post(self, request):
        username = request.POST['username']
        pword1 = request.POST['password1']
        pword2 = request.POST['password2']
        try:
            user = get_object_or_404(UserAccountsModel, username=username)
            assert_immutable_user(user)
            if pword1 == pword2:
                user.set_password(pword2)
                user.save()
                msg.success(request, 'Password changed successfully!')
            else:
                msg.error(request, 'Password does not match!')
        except Http404:
            msg.error(request, 'Username does not exist!')
        return redirect('user_accounts:manage_users')


class DeleteUser(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'user_accounts.delete_user'
    model = UserAccountsModel
    success_url = 'user_accounts:manage_users'
    values_list = 'username'


#########################################
#       USER ROLES
########################################
class CreateRole(PermissionRequiredMixin, View):
    perm = 'user_accounts.manage_roles'

    def get(self, request):
        form = CreateRoleForm()
        return render(request, 'user_accounts/create_role.html', {'role': form})

    def post(self, request):
        form = CreateRoleForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                msg.success(request, 'Role created successfully!')
                return redirect('user_accounts:create_role')
        except IntegrityError:
            msg.error(request, 'Role name already exists!')
            return render(request, 'user_accounts/create_role.html', {'role': form})


class UpdateRole(PermissionRequiredMixin, View):
    perm = 'user_accounts.manage_roles'

    def get(self, request, pk):
        form = UpdateRoleForm(data=get_group_perms(get_object_or_404(Group, pk=pk)))
        return render(request, 'user_accounts/update_role.html', {'role': form})

    def post(self, request, *args, **kwargs):
        form = UpdateRoleForm(request.POST)
        if form.is_valid():
            form.save()
            msg.success(request, 'Role updated successfully!')
            return redirect('user_accounts:manage_roles')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, 'user_accounts/update_role.html', {'role': form})


class ManageRoles(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'user_accounts.manage_roles'
    template = 'user_accounts/manage_roles.html'
    model = Group
    url_filter_kwargs = (
        ('search', 'name__icontains'),
    )
    order_col = 'id'
    values_list_cols = ('id', 'name')


class DeleteRole(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'user_accounts.manage_roles'
    model = Group
    success_url = 'user_accounts:manage_roles'
    values_list = 'name'
