from django import forms
from .models import Contacto, Historial_Transfer, Historial_Commer, UserProfile
from django.contrib.auth.forms import UserCreationForm

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields= ['nombre', 'corre', 'tipo_consulta','mensaje', 'avisos' ]

class TransferForm(forms.ModelForm):
    class Meta:
        model = Historial_Transfer
        fields= ['receptor_email','receptor_name','monto','moneda']


class CommerForm(forms.ModelForm):
    class Meta:
        model = Historial_Commer
        fields= ['monto','moneda','accion']

class RegistroForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields= ['name' , 'email' , 'BTC_Count','XRP_Count','DOGE_Count','USD_Count']



