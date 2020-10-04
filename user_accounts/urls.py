from django.urls import path
from . import views

app_name = 'user_accounts'
urlpatterns = [
    path('create-account/', views.CreateUserAccount.as_view(), name='create_user_account'),
    path('manage-users/', views.ManageUserAccount.as_view(), name='manage_users'),
    path('toggle-user-status/', views.ToggleUserStatus.as_view(), name='toggle_user_status'),
    path('delete-user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
    path('update-user-account/<int:pk>/', views.UpdateUserAccount.as_view(), name='update_user')
]
