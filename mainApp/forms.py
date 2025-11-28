from django import forms
from mainApp.models import Pedido

class FormPedido(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['nombre','email','telefono','producto','descripcion','imagen','origen','fecha_necesitado','cantidad'] 
    
