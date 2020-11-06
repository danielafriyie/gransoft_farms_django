from django.urls import path, include

from .views import (
    MainModule, ManagePenhouseView, DeletePenhouseView, UpdatePenhouseView, ManageStockView,
    DeleteStockView, UpdateStockView, ManageMortCullView, DeleteMortCullView, UpdateMortcullView,
    ManageMedicineFeedView, UpdateMedicineFeedView, DeleteMedicineView
)

app_name = 'birds'

main_module_url = [
    path('', MainModule.as_view(), name='main_module')
]

penhouse_url_patterns = [
    path('penhouse/', include([
        path('manage-penhouse', ManagePenhouseView.as_view(), name='manage_penhouse'),
        path('update-penhouse/<int:pk>/', UpdatePenhouseView.as_view(), name='update_penhouse'),
        path('delete-penhouse/<int:pk>/', DeletePenhouseView.as_view(), name='delete_penhouse')
    ]))
]

stock_url_patterns = [
    path('stock/', include([
        path('manage-stock', ManageStockView.as_view(), name='manage_stock'),
        path('update-stock/<int:pk>/', UpdateStockView.as_view(), name='update_stock'),
        path('delete-stock/<int:pk>/', DeleteStockView.as_view(), name='delete_stock')
    ]))
]

mort_cull_url_patterns = [
    path('mort-cull/', include([
        path('manage/', ManageMortCullView.as_view(), name='manage_mort_cull'),
        path('update/<int:pk>/', UpdateMortcullView.as_view(), name='update_mort_cull'),
        path('delete/<int:pk>/', DeleteMortCullView.as_view(), name='delete_mort_cull')
    ]))
]

med_feed_url_patterns = [
    path('med-feed/', include([
        path('manage/', ManageMedicineFeedView.as_view(), name='manage_med_feed'),
        path('update/<int:pk>/', UpdateMedicineFeedView.as_view(), name='update_med_feed'),
        path('delete/<int:pk>/', DeleteMedicineView.as_view(), name='delete_med_feed')
    ]))
]

urlpatterns = main_module_url + penhouse_url_patterns + stock_url_patterns + mort_cull_url_patterns + \
              med_feed_url_patterns
