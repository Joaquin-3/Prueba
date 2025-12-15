from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido, Insumo
from mainApp.forms import FormPedido
from django.db import IntegrityError, DatabaseError

from rest_framework import generics
from rest_framework.response import Response
from .serializers import InsumoSerializer, PedidoSerializer

from rest_framework.views import APIView
from datetime import datetime

# Create your views here.

def home(request):
    categoria = Categoria.objects.all()
    productos = Producto.objects.all()
    data = {'categoria': categoria, 'productos': productos}
    
    return render(request, 'home.html',data)

def productos(request, categoria_slug):
    categoria = Categoria.objects.get(slug=categoria_slug)
    productos = Producto.objects.filter(categoria=categoria)

    data = {
        'categoria': categoria,
        'productos': productos
    }

    return render(request, 'productos.html', data)


def detalle(request, producto_slug):
    producto = get_object_or_404(Producto, slug=producto_slug)

    data = {'producto': producto}

    return render(request, 'detalle.html', data)

def pedido(request, producto_slug=None):
    producto_preseleccionado = None
    if producto_slug:
        producto_preseleccionado = get_object_or_404(Producto, slug=producto_slug)

    if request.method == "POST":
        form = FormPedido(request.POST, request.FILES, producto_inicial=producto_preseleccionado)

        if form.is_valid():
            pedido = form.save(commit=False)

            if producto_preseleccionado:
                pedido.producto = producto_preseleccionado

            try:
                pedido.save()
                url = request.build_absolute_uri(f"/seguimiento/{pedido.token}/")
                return render(request, "pedido_creado.html", {
                    "token": pedido.token,
                    "url": url
                })
            except IntegrityError as e:
                form.add_error(None, "Error de integridad en la base de datos. Revise los datos ingresados.")
            except DatabaseError as e:
                form.add_error(None, "Error al guardar en la base de datos. Intente nuevamente.")
            except Exception as e:
                form.add_error(None, f"Ocurrió un error inesperado: {str(e)}")

    else:
        form = FormPedido(producto_inicial=producto_preseleccionado)

    return render(request, "formulario.html", {
        "form": form,
        "producto_preseleccionado": producto_preseleccionado
    })

def seguimiento(request, token=None):
    if token is None:
        token = request.GET.get("token", "")

    pedido = get_object_or_404(Pedido, token=token)

    data = {
        "pedido": pedido
    }
    return render(request, "seguimiento.html", data)


class InsumoListCreateAPI(generics.ListCreateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

class InsumoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


class PedidoCreateAPI(generics.CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_field = 'token'


class PedidoFiltroAPI(APIView):

    def post(self, request):
        pedidos = Pedido.objects.all()

        fecha_inicio = request.data.get('fecha_inicio')
        fecha_entrega_requerida = request.data.get('fecha_entrega_requerida')
        estados = request.data.get('estados')

        if fecha_inicio and fecha_entrega_requerida:
            pedidos = pedidos.filter(
                fecha_pedido__gte=fecha_inicio,
                fecha_pedido__lte=fecha_entrega_requerida
            )

        if estados:
            if isinstance(estados, list):
                pedidos = pedidos.filter(estado__in=estados)
            else:
                pedidos = pedidos.filter(estado=estados)



        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)