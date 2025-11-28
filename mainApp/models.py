from django.db import models
from django.utils.html import format_html



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre


class Estado(models.TextChoices):
    SOLICITADO = 'Solicitado', 'Solicitado'
    APROBADO = 'Aprobado', 'Aprobado'
    EN_PROCESO = 'En Proceso', 'En Proceso'
    REALIZADO = 'Realizado', 'Realizado'
    ENTREGADO = 'Entregado', 'Entregado'
    FINALIZADO = 'Finalizado', 'Finalizado'
    CANCELADO = 'Cancelado', 'Cancelado'


class Origen(models.TextChoices):
    FACEBOOK = 'Facebook', 'Facebook'
    INSTAGRAM = 'Instagram', 'Instagram'
    PRESENCIAL = 'Presencial', 'Presencial'
    WHATSAPP = 'WhatsApp', 'WhatsApp'
    SITIO_WEB = 'Sitio Web', 'Sitio Web'
    TIKTOK = 'TikTok', 'TikTok'


class EstadoPago(models.TextChoices):
    PENDIENTE = 'Pendiente', 'Pendiente'
    PARCIAL = 'Parcial', 'Parcial'
    PAGADO = 'Pagado', 'Pagado'



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    imagen1 = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre


class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    marca = models.CharField(max_length=100)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.SOLICITADO
    )

    origen = models.CharField(
        max_length=20,
        choices=Origen.choices,
        default=Origen.PRESENCIAL
    )

    estado_pago = models.CharField(
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE
    )
            

    def fin(self):
        if self.estado == Estado.FINALIZADO:
            if self.estado_pago == EstadoPago.PAGADO:
                return True
            else:
                return 'No se encuentra pagado'
        else: 
            return False

    def __str__(self):
        return f"Pedido de {self.cantidad} x {self.producto.nombre}"

