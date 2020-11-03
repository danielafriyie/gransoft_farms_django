from django.urls import path
from .views import (
    CreateFinanceItemView, ManageFinanceItemView, DeleteFinanceItemView, UpdateFinanceItemView, MainModuleMixin
)

app_name = 'finance'

urlpatterns = [
    path('', MainModuleMixin.as_view(), name='main_module'),
    path('create/', CreateFinanceItemView.as_view(), name='create'),
    path('update/', UpdateFinanceItemView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteFinanceItemView.as_view(), name='delete'),
    path('manage/', ManageFinanceItemView.as_view(), name='manage')
]
