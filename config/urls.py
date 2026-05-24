# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # El panel clásico de Django
    path('', include('biblioteca.urls')),     # Incluye todas las rutas de tu app biblioteca
]

# Servir archivos multimedia (portadas) en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)