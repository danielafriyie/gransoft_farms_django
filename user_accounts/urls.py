from django.urls import path
from .views import (
    CreateUserAccount, ManageUserAccount, ToggleUserStatus, DeleteUser, UpdateUserAccount,
    SetUserPassword, ManageRoles, DeleteRole, CreateRole, UpdateRole
)

app_name = 'user_accounts'
urlpatterns = [
    path('create-account/', CreateUserAccount.as_view(), name='create_user_account'),
    path('manage-users/', ManageUserAccount.as_view(), name='manage_users'),
    path('toggle-user-status/', ToggleUserStatus.as_view(), name='toggle_user_status'),
    path('delete-user/<int:pk>/', DeleteUser.as_view(), name='delete_user'),
    path('update-user-account/<int:pk>/', UpdateUserAccount.as_view(), name='update_user'),
    path('set-password/', SetUserPassword.as_view(), name='set_user_password'),
    path('manage-roles/', ManageRoles.as_view(), name='manage_roles'),
    path('create-role/', CreateRole.as_view(), name='create_role'),
    path('update-role/<int:pk>/', UpdateRole.as_view(), name='update_role'),
    path('delete-role/<int:pk>/', DeleteRole.as_view(), name='delete_role')
]
