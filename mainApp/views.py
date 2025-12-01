from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria, Pedido
from mainApp.forms import FormPedido
from django.db import IntegrityError, DatabaseError

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
