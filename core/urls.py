from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('user-accounts/', include('user_accounts.urls')),
    path('finance/', include('finance.urls')),
    path('reports/', include('reports.urls')),
    path('birds/', include('birds.urls')),
    path('gransoft-farms-admin-code-efc123go9090/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
