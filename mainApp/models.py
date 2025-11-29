from django.db import models
import uuid


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
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=15, decimal_places=0)

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
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.IntegerField(null=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=70)
    cantidad = models.IntegerField()
    token = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    fecha_pedido = models.DateField(auto_now_add=True)
    fecha_necesitado = models.DateField(null=True)

    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    origen = models.CharField(
        max_length=20,
        choices=Origen.choices,
        default=Origen.SITIO_WEB
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.SOLICITADO
    )

    estado_pago = models.CharField(
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE
    )

    def precio_final(self):
        if self.producto and self.cantidad:
            return self.producto.precio * self.cantidad
        return 0

def __str__(self):
        return f"Pedido de {self.cantidad} x {self.producto.nombre} - Total: ${self.precio_final}"

