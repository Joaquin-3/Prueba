from django import forms
from mainApp.models import Pedido, Categoria

class FormPedido(forms.ModelForm):

    categoria_personalizada = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False
    )

    class Meta:
        model = Pedido
        fields = [
            'nombre', 'email', 'telefono',
            'producto', 'descripcion', 'imagen',
            'fecha_entrega_requerida', 'cantidad'
        ]

    def __init__(self, *args, **kwargs):
        producto_inicial = kwargs.pop("producto_inicial", None)
        super().__init__(*args, **kwargs)


        if producto_inicial:
            self.fields["producto"].widget = forms.HiddenInput()
            self.fields["producto"].initial = producto_inicial

            self.fields["imagen"].widget = forms.HiddenInput()
            self.fields["imagen"].required = False

            self.fields["categoria_personalizada"].widget = forms.HiddenInput()
            self.fields["categoria_personalizada"].required = False



        else:
            self.fields["producto"].widget = forms.HiddenInput()
            self.fields["producto"].required = False

            self.fields["imagen"].required = True

            self.fields["categoria_personalizada"].required = True
