from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('categoria/<slug:categoria_slug>/', views.productos, name='productos_por_categoria')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)