from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import UserAccountsModel, UserAccountsModelAudit, UsersAuthenticationLog


class CreateUserAccountForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserAccountsModel
        fields = (
            'name', 'username', 'phone_no', 'gender', 'date_of_birth',
            'is_admin', 'is_staff', 'is_superuser', 'is_immutable', 'auth_user'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserAccountForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserAccountsModel
        fields = (
            'name', 'username', 'phone_no', 'gender', 'date_of_birth',
            'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'is_immutable', 'auth_user'
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(UserAccountsModel)
class UserAccountsAdmin(UserAdmin):
    form = UpdateUserAccountForm
    add_form = CreateUserAccountForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone_no', 'gender', 'date_of_birth', 'auth_user')}),
        (_('Permissions'), {
            'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'is_immutable', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('date_created',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'username', 'phone_no', 'gender', 'date_of_birth',
                'is_admin', 'is_staff', 'is_superuser', 'is_immutable', 'auth_user',
                'password1', 'password2'
            )
        }),
    )

    list_display = (
        'id', 'username', 'name', 'phone_no', 'gender', 'date_of_birth',
        'date_created', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'is_immutable'
    )
    list_display_links = ('id', 'username')
    readonly_fields = ('date_created',)
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('date_created', 'gender')
    search_fields = ('id', 'username', 'date_created')
    list_per_page = 25


@admin.register(UserAccountsModelAudit)
class UserAccountsAuditAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'name', 'phone_no', 'gender', 'date_of_birth',
        'date_created', 'is_admin', 'is_active', 'is_staff', 'is_superuser'
    )
    list_display_links = ('id', 'username')
    list_filter = ('date_created', 'gender')
    search_fields = ('id', 'username', 'date_created')
    list_per_page = 25


@admin.register(UsersAuthenticationLog)
class UsersAuthenticationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'auth_user', 'last_login', 'last_logout')
    list_display_links = ('id', 'auth_user')
    search_fields = ('auth_user',)
    list_per_page = 25
