from django import forms


class BaseAuthForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)

    # styling form widgets
    username.widget.attrs.update({'class': 'user-credentials form-control', 'placeholder': 'username'})
    password.widget.attrs.update({'class': 'user-credentials form-control', 'placeholder': 'password'})


class LoginForm(BaseAuthForm):
    pass


class ChangePasswordForm(BaseAuthForm):
    new_password = forms.CharField(required=True, max_length=100, widget=forms.PasswordInput)
    new_password.widget.attrs.update({
        'class': 'user-credentials form-control', 'placeholder': 'new password', 'minlength': '6'
    })
