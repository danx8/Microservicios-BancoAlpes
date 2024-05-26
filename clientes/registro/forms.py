from django import forms
from clientes.models import Cliente

class ClienteFormRegistro(forms.ModelForm):
    terminosYCondiciones = forms.BooleanField(label='Acepto los términos y condiciones', required=True)
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'cedula', 
            'celular',
            'correo',
            'pais',
            'ciudad',
            'fechaNacimiento'

        ]
        labels = {
            'nombre' : 'Nombre',
            'apellido' : 'Apellido',
            'cedula' : 'Cedula',
            'celular' : 'Celular',
            'correo' : 'Correo',
            'pais' : 'Pais',
            'ciudad' : 'Ciudad',
            'fechaNacimiento' : 'Fecha de nacimiento',
        }

        widgets = {
            'fechaNacimiento': forms.DateInput(attrs={'type': 'date'})
        }
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
       
        self.fields['terminosYCondiciones'].widget.attrs.update({'class': 'custom-checkbox'})

    def clean(self):
        cleaned_data = super().clean()
        terms_and_conditions = cleaned_data.get('terminosYCondiciones')
        
        if not terms_and_conditions:
            self.add_error('terminosYCondiciones', 'Debes aceptar los términos y condiciones para continuar.')
        
        return cleaned_data
    