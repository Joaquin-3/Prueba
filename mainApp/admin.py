from django.contrib import admin
from .models import Categoria, Producto, Insumo, Pedido
from django.core.exceptions import ValidationError

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio')
    prepopulated_fields = {'slug': ('nombre',)}
    list_filter = ('categoria',)


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

    def save_model(self, request, obj, form, change):
        if obj.estado == "Finalizado" and obj.estado_pago != "Pagado":
            raise ValidationError("No puedes finalizar un pedido si no está pagado completamente.")
        super().save_model(request, obj, form, change)