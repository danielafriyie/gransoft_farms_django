from django.urls import path
from .views import logout_view, home, login_view, change_password

app_name = 'home'
urlpatterns = [
    path('', login_view, name='login'),
    path('home/', home, name='homepage'),
    path('logout/', logout_view, name='logout'),
    path('change-password', change_password, name='change_password')
]
