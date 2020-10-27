from django.urls import path, include

from .views import (
    MainModule, ManagePenhouseView, DeletePenhouseView
)

app_name = 'birds'

main_module_url = [
    path('', MainModule.as_view(), name='main_module')
]

penhouse_url_patterns = [
    path('penhouse/', include([
        path('manage-penhouse', ManagePenhouseView.as_view(), name='manage_penhouse'),
        path('delete-penhouse/<int:pk>/', DeletePenhouseView.as_view(), name='delete_penhouse')
    ]))
]

urlpatterns = main_module_url + penhouse_url_patterns
