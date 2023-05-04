from django.contrib import admin
from django.urls import path, include
from automated_system_statusbank.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('statusbanksystem/', include('automated_system_statusbank.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
