from django.urls import path
from . import views

app_name = 'user_accounts'
urlpatterns = [
    path('create-account', views.CreateUserAccount.as_view(), name='create_user_account')
]
