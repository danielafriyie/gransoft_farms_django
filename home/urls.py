from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='homepage'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password', views.change_password, name='change_password')
]
