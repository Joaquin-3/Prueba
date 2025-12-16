from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('categoria/<slug:categoria_slug>/', views.productos, name='productos_por_categoria'),
    path('detalle/<slug:producto_slug>/', views.detalle, name='detalle'),
    path('pedidos/add',views.pedido, name='pedido'),
    path('seguimiento/<slug:token>/', views.seguimiento, name='seguimiento'),
    path('pedidos/add/', views.pedido, name='pedido'),
    path('pedidos/add/<slug:producto_slug>/', views.pedido, name='pedido_con_producto'),
    path("reporte/", views.reporte_pedidos, name="reporte_pedidos"),


    path('api/insumos/', views.InsumoListCreateAPI.as_view()),
    path('api/insumos/<int:pk>/', views.InsumoDetailAPI.as_view()),

    path('api/pedidos/filtrar/', views.PedidoFiltroAPI.as_view()),
    path('api/pedidos/', views.PedidoCreateAPI.as_view()),
    path('api/pedidos/<slug:token>/', views.PedidoUpdateAPI.as_view()),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)