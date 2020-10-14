from django.urls import path, include
from .views import (
    CreatePurchase, ManagePurchases, DeletePurchase, UpdatePurchase
)

app_name = 'finance'

purchase_urls = [
    path('purchases/', include([
        path('create-purchase/', CreatePurchase.as_view(), name='create_purchase'),
        path('update-purchase/', UpdatePurchase.as_view(), name='update_purchase'),
        path('delete-purchase/<int:pk>/', DeletePurchase.as_view(), name='delete_purchase'),
        path('manage-purchases/', ManagePurchases.as_view(), name='manage_purchases'),
    ]))
]

urlpatterns = purchase_urls
