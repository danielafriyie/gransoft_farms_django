from django import forms

from .models import UserAccountsModel
from utils import assign_user_roles

form_widgets = {
    'name': forms.TextInput(attrs={'class': 'form-input form-control'}),
    'phone_no': forms.TextInput(attrs={'class': 'form-input form-control'}),
    'gender': forms.Select(attrs={'class': 'form-input form-control'}),
    'date_of_birth': forms.DateInput(attrs={'class': 'form-input form-control', 'type': 'date'}),
    'username': forms.TextInput(attrs={'class': 'form-input form-control'}),
    'password': forms.PasswordInput(attrs={'class': 'form-control', 'minlength': 6, 'maxlength': 25}),
}


class AccessRightsForm(forms.Form):
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
        if self.is_valid():
            self.form_data = {
                'admin': self.cleaned_data.get('admin', False),
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
    instance_user = None

    class Meta:
        model = UserAccountsModel
        widgets = form_widgets
        fields = (
            'name', 'phone_no', 'gender', 'date_of_birth', 'username', 'password'
        )
        abstract = True

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

    def save(self, roles):
        if not self.instance_user:
            raise ValueError("'instance_user' is not defined")
        if not isinstance(roles, dict):
            raise ValueError(f"'roles' is not an instance of {dict}")
        user = UserAccountsModel.objects.create_user(**self.get_form_data)
        assign_user_roles(user, roles)
