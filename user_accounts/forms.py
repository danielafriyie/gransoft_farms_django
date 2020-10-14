from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission

from .models import UserAccountsModel


class BaseRoleForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'name'}), required=True)

    # user account permissions
    check_all = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    add_user = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    update_user = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    delete_user = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    set_password = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    manage_roles = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    view_user_account_audit_trail = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'}), required=False)

    # finance permissions
    finance_pur_add_new = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                             required=False)
    finance_pur_update = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                            required=False)
    finance_pur_delete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                            required=False)
    finance_pur_audit_trail = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                                 required=False)
    finance_pur_report = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                            required=False)

    @property
    def get_form_data(self):
        if self.is_valid():
            self.form_data = {
                'name': self.cleaned_data['name'],
                'add_user': self.cleaned_data['add_user'],
                'update_user': self.cleaned_data['update_user'],
                'delete_user': self.cleaned_data['delete_user'],
                'set_password': self.cleaned_data['set_password'],
                'manage_roles': self.cleaned_data['manage_roles'],
                'view_user_account_audit_trail': self.cleaned_data['view_user_account_audit_trail'],
                'finance_pur_add_new': self.cleaned_data['finance_pur_add_new'],
                'finance_pur_update': self.cleaned_data['finance_pur_update'],
                'finance_pur_delete': self.cleaned_data['finance_pur_delete'],
                'finance_pur_audit_trail': self.cleaned_data['finance_pur_audit_trail'],
                'finance_pur_report': self.cleaned_data['finance_pur_report']
            }
        return self.form_data

    def assign_role(self, group):
        form_data = self.get_form_data
        form_data.pop('name')

        for role in form_data:
            if form_data[role]:
                group.permissions.add(get_object_or_404(Permission, codename=role))


class CreateRoleForm(BaseRoleForm):

    def save(self):
        group = Group.objects.create(name=self.get_form_data['name'])
        self.assign_role(group)


class UpdateRoleForm(BaseRoleForm):

    def save(self):
        group = get_object_or_404(Group, name=self.get_form_data['name'])
        group.permissions.clear()
        self.assign_role(group)


class BaseUserAccountsForm(forms.ModelForm):
    instance_user = None

    class Meta:
        model = UserAccountsModel
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'minlength': 6, 'maxlength': 25}),
        }
        fields = (
            'name', 'phone_no', 'gender', 'date_of_birth', 'username', 'password'
        )

    @property
    def get_form_data(self):
        return {
            'username': self.cleaned_data.get('username', False),
            'password': self.cleaned_data.get('password', False),
            'name': self.cleaned_data.get('name', False),
            'phone_no': self.cleaned_data.get('phone_no', False),
            'gender': self.cleaned_data.get('gender', False),
            'date_of_birth': self.cleaned_data.get('date_of_birth', False),
            'auth_user': self.instance_user
        }


class CreateUserAccountForm(BaseUserAccountsForm):

    def save(self, role):
        if not self.instance_user:
            raise ValueError("'instance_user' is not defined")
        user = UserAccountsModel.objects.create_user(**self.get_form_data)
        if role:
            group = get_object_or_404(Group, name=role)
            group.user_set.add(user)


class UpdateUserAccountForm(BaseUserAccountsForm):
    class Meta(BaseUserAccountsForm.Meta):
        fields = (
            'name', 'phone_no', 'gender', 'date_of_birth'
        )

    def save(self, pk, role) -> None:
        if not self.instance_user:
            raise ValueError("'instance_user' is not defined")
        user = get_object_or_404(UserAccountsModel, pk=pk)
        user.name = self.get_form_data['name']
        user.phone_no = self.get_form_data['phone_no']
        user.gender = self.get_form_data['gender']
        user.date_of_birth = self.get_form_data['date_of_birth']
        user.auth_user = self.instance_user
        user.groups.clear()
        if role:
            group = get_object_or_404(Group, name=role)
            user.groups.add(group)
        user.save()
