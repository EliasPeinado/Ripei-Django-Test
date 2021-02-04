from django.shortcuts import render, redirect
from .models import Crito, UserProfile
from .forms import ContactoForm, TransferForm, CommerForm, RegistroForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import CritoSerializer

class CritoViewset(viewsets.ModelViewSet):
    queryset = Crito.objects.all()
    serializer_class = CritoSerializer

    def get_queryset(self):
        criptos = Crito.objects.all()
 
        exist = self.request.GET.get('name').exists()
        if exist:
            name = self.request.GET.get('name')
            criptos = criptos.filter(name = name)
        

        return criptos


def home (request):
    return render(request,'app/home.html')

def info (request):
    return render(request,'app/info.html')

def contacto (request):
    data = {
        'data': ContactoForm (),
        'mensaje': ''
    }
    

    if request.method == 'POST':
        formulario =  ContactoForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Formulario enviado correctamente'
        else:
            data['mensaje'] = 'El formulario no se pudo enviar'
            data['form'] = formulario

    return render(request, 'app/contacto.html', data)

def commercialize (request):

    
    Criptos = Crito.objects.all()

    
    data = {
        'data' :Criptos
    }
    return render(request, 'app/commercialize.html', data)

def transferir (request):

    data = {
        'form': TransferForm()
    }
    if request.method == 'POST':

        request.POST._mutable = True
        request.POST.pop('csrfmiddlewaretoken')
        request.POST['emisor_email'] = '' #User.email
        request.POST['emisor_name'] = '' #User.first_name
        request.POST._mutable = False 
        formulario =  TransferForm(data = request.POST)

        if formulario.is_valid():
            function = CoinOperations(moneda= request.POST['moneda'],accion= 0, monto= request.POST['monto'], email= request.POST['receptor_email'])
            formulario.save()
            data['mensaje'] = function

        else:
            data['form'] = formulario
            data['mensaje'] = 'ocurrio un error, contacte con soporte!'
    return render(request, 'app/transferir.html', data)

def CoinOperations(moneda, accion, monto, email ):

    try:    
        exist = UserProfile.objects.all().filter(email= email).exists()
        if exist:
            crpitos = Crito.objects.all()
            user = UserProfile.objects.all().get(email= email)
            if int(moneda) == 0:#-------------------------------------------------------------------------------------
                crpitos.filter(name = 'Bitcoin')
                crpito = crpitos[0]
                if crpito*int(monto) < user.USD_Count:
                    if int(accion) == 0:
                        user.BTC_Count += int(monto) 
                    else:
                        user.BTC_Count -= int(monto)
                else:
                    return 'Dinero insuficiente, compre dolares!'
            elif int(moneda) == 1:#-------------------------------------------------------------------------------------
                crpitos.filter(name = 'XRP')
                crpito = crpitos[0]
                if crpito*int(monto) < user.USD_Count:
                    if int(accion) == 0:
                        user.XRP_Count += int(monto)
                    else:
                        user.XRP_Count -= int(monto)
                else:
                    return 'Dinero insuficiente, compre dolares!'
            elif int(moneda) == 2:#-------------------------------------------------------------------------------------
                crpitos.filter(name = 'Dogecoin')
                crpito = crpitos[0]
                if crpito*int(monto) < user.USD_Count:
                    if int(accion) == 0:
                        user.DOGE_Count += int(monto)
                    else:
                        user.DOGE_Count -= int(monto)
                else:
                    return 'Dinero insuficiente, compre dolares!'
            elif int(moneda) == 3:#-------------------------------------------------------------------------------------
                if int(accion) == 0:
                    user.USD_Count += int(monto)
                else:
                    user.USD_Count -= int(monto)
            user.save()
            return ('Transferencia enviada con exito!')
        else:
            return ('El usuario no existe!')
    except:    
         return ('ocurrio un error, contacte con soporte!')
    

def buySell (request):

    
    data = {
        'form': CommerForm()
    }
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['email'] = User.email
        request.POST.pop('csrfmiddlewaretoken')
        request.POST._mutable = False 
        formulario =  CommerForm(data= request.POST)


        if formulario.is_valid():
            CoinOperations(moneda= request.POST['moneda'],accion= request.POST['accion'], monto= request.POST['monto'], email= request.POST['email'])
            formulario.save()
            data['mensaje'] = 'Transferencia enviada con exito!'
        else:
            data['form'] = formulario
            data['mensaje'] = 'ocurrio un error, contacte con soporte!'
    return render(request,'app/buySell.html', data)


def registro (request):
    data = {
        'form' : RegistroForm()
    }
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST.pop('csrfmiddlewaretoken')
        request.POST._mutable = False 
        formulario =  RegistroForm(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Registrado con exito'
            return redirect(to = 'home')
        else:
           data['form'] = formulario
           data['mensaje'] = request.POST.GET
    return render(request,'app/registro.html', data)