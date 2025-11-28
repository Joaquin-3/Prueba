from django.shortcuts import render

from .models import Producto, Categoria, Insumo, Pedido
# Create your views here.

def home(request):
    categoria = Categoria.objects.all()
    data = {'categoria': categoria}
    return render(request, 'home.html',data)

def productos(request, categoria_slug):
    categoria = Categoria.objects.get(slug=categoria_slug)
    productos = Producto.objects.filter(categoria=categoria)

    data = {
        'categoria': categoria,
        'productos': productos
    }

    return render(request, 'productos.html', data)
