from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido
from mainApp.forms import FormPedido
import uuid

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

def pedido(request):
    form = FormPedido()

    if request.method == 'POST':
        form = FormPedido(request.POST, request.FILES)

        if form.is_valid():
            pedido = form.save(commit=False)

            pedido.token = uuid.uuid4().hex[:12]                     
            pedido.save()

            url_seguimiento = request.build_absolute_uri(
                f"/seguimiento/{pedido.token}/"
            )

            return render(
            request,
            "pedido_creado.html",
            {
                "url": url_seguimiento,
                "token": pedido.token
            }
            )

    data = {'form': form}
    return render(request, 'formulario.html', data)

def seguimiento(request, token=None):
    if token is None:
        token = request.GET.get("token", "")

    pedido = get_object_or_404(Pedido, token=token)

    data = {
        "pedido": pedido
    }
    return render(request, "seguimiento.html", data)
