from django.contrib import admin
from .models import Categoria, Producto, Insumo, Pedido
from django.core.exceptions import ValidationError
from django.utils.html import format_html

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio','ver_imagen')
    prepopulated_fields = {'slug': ('nombre',)}
    list_filter = ('categoria',)
    readonly_fields = ['ver_imagen']

    def ver_imagen(self, obj):

        if obj.imagen1:  
            return format_html('<img src="{}" width="50" height="50" />', obj.imagen1.url)
        elif obj.imagen2:
            return format_html('<img src="{}" width="50" height="50" />', obj.imagen2.url)
        elif obj.imagen3:
            return format_html('<img src="{}" width="50" height="50" />', obj.imagen3.url)
        else:
            return "No disponible"

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cantidad', 'marca', 'color')
    search_fields = ('nombre', 'tipo', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha_pedido', 'estado', 'origen', 'estado_pago')
    list_filter = ('fecha_pedido',)
    search_fields = ('producto__nombre',)
    readonly_fields = ['ver_imagen']

    def save_model(self, request, obj, form, change):
        if obj.estado == "Finalizado" and obj.estado_pago != "Pagado":
            raise ValidationError("No puedes finalizar un pedido si no está pagado completamente.")
        super().save_model(request, obj, form, change)


    def ver_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" />', obj.imagen.url)
        return "No disponible"