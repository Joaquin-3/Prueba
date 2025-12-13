from rest_framework import serializers
from .models import Categoria, Producto, Pedido ,Insumo

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    precio_final = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['token', 'fecha_pedido']

    def get_precio_final(self, obj):
        return obj.precio_final()
