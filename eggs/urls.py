from django.urls import path
from .views import ManageEggsView, MainModuleView, UpdateEggView, DeleteEggView

app_name = 'eggs'
urlpatterns = [
    path('', MainModuleView.as_view(), name='main_module'),
    path('manage-egg/', ManageEggsView.as_view(), name='manage_eggs'),
    path('update-egg/<int:pk>/', UpdateEggView.as_view(), name='update_egg'),
    path('delete-egg/<int:pk>/', DeleteEggView.as_view(), name='delete_egg')
]
