from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('image_processor.urls')),  # Enlaza con las rutas de la app
]
