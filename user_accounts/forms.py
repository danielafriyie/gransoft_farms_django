from django import forms
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import UserAccountsModel
from utils import assign_user_roles

User = settings.AUTH_USER_MODEL
form_widgets = {
    'name': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Name'}),
    'phone_no': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Phone'}),
    'gender': forms.Select(attrs={'class': 'custom-form-control', 'placeholder': 'Gender'}),
    'date_of_birth': forms.DateInput(attrs={
        'class': 'custom-form-control', 'type': 'date', 'placeholder': 'Birthdate'}),
    'username': forms.TextInput(attrs={'class': 'custom-form-control', 'placeholder': 'Username'}),
    'password': forms.PasswordInput(attrs={
        'class': 'custom-form-control', 'minlength': 6, 'maxlength': 25, 'placeholder': 'Password'}),
}


class AccessRightsForm(forms.Form):
    auth_user = None  # type: User

    admin = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    user_create = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    user_update = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    user_delete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    fowls_create = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    fowls_update = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    fowls_delete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    finance_create = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    finance_update = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    finance_delete = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    @property
    def get_form_data(self):
        if not self.auth_user:
            raise ValueError("'auth_user' is not defined")
        if self.is_valid():
            self.form_data = {
                'admin': self.cleaned_data.get('admin', False) if self.auth_user.is_admin else False,
                'user_create': self.cleaned_data.get('user_create', False),
                'user_update': self.cleaned_data.get('user_update', False),
                'user_delete': self.cleaned_data.get('user_delete', False),
                'fowls_create': self.cleaned_data.get('fowls_create', False),
                'fowls_update': self.cleaned_data.get('fowls_update', False),
                'fowls_delete': self.cleaned_data.get('fowls_delete', False),
                'finance_create': self.cleaned_data.get('finance_create', False),
                'finance_update': self.cleaned_data.get('finance_update', False),
                'finance_delete': self.cleaned_data.get('finance_delete', False)
            }
        return self.form_data


class BaseUserAccountsForm(forms.ModelForm):
    instance_user = None  # type: User

    class Meta:
        model = UserAccountsModel
        widgets = form_widgets
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

    def save(self, roles: dict) -> None:
        if not self.instance_user:
            raise ValueError("'instance_user' is not defined")
        if not isinstance(roles, dict):
            raise ValueError(f"'roles' is not an instance of {dict}")
        user = UserAccountsModel.objects.create_user(**self.get_form_data)
        assign_user_roles(user, roles)


class UpdateUserAccountForm(BaseUserAccountsForm):
    class Meta(BaseUserAccountsForm.Meta):
        fields = (
            'name', 'phone_no', 'gender', 'date_of_birth'
        )

    def save(self, pk: int, roles: dict) -> None:
        if not self.instance_user:
            raise ValueError("'instance_user' is not defined")
        if not isinstance(roles, dict):
            raise ValueError(f"'roles' is not an instance of {dict}")
        user = get_object_or_404(UserAccountsModel, pk=pk)
        user.name = self.get_form_data['name']
        user.phone_no = self.get_form_data['phone_no']
        user.gender = self.get_form_data['gender']
        user.date_of_birth = self.get_form_data['date_of_birth']
        user.auth_user = self.instance_user
        user.save()
        assign_user_roles(user, roles)
