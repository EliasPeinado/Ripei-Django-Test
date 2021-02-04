from django.shortcuts import render, redirect
from .models import Crito, UserProfile
from .forms import ContactoForm, TransferForm, CommerForm, RegistroForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import CritoSerializer
import sys

class CritoViewset(viewsets.ModelViewSet):
    queryset = Crito.objects.all()
    serializer_class = CritoSerializer

    def get_queryset(self):
        criptos = Crito.objects.all()
 

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
#Muestra las Criptomonedas habilitadas para comercializar
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

        #Modifico el form para poder guardarlo correctamente en la BBDD
        request.POST._mutable = True
        request.POST.pop('csrfmiddlewaretoken')
        # request.POST['emisor_email'] = '' #User.email
        # request.POST['emisor_name'] = '' #User.first_name
        request.POST._mutable = False 
        formulario =  TransferForm(data = request.POST)

        #Si el formulario es valido, llamo a la funcion CoinOperations para que haga la transferencia (comente email_emis porque no esta funcionando el login)
        if formulario.is_valid():
            function = CoinOperations(
                moneda= request.POST['moneda'],
                accion= 0,
                monto= request.POST['monto'],
                email= request.POST['receptor_email'])
                #, email_emis= User.email)
            formulario.save() 
            data['mensaje'] = function

        else:
            data['form'] = formulario
            data['mensaje'] = 'ocurrio un error, contacte con soporte!'
    return render(request, 'app/transferir.html', data)

#La funcion CoinOperations se encarga las acciones de enviar, comprar o vender criptos o USD
def CoinOperations(moneda, accion, monto, email, email_emis = 'null' ):

    try:    

            crpitos = Crito.objects.all()
            user = UserProfile.objects.all().get(email= email)
            if email_emis != 'null':
                user_emi = UserProfile.objects.all().get(email= email_emis)

            if float(moneda) == 0:#-------------------------------------------------------------------------------------
                
                crpito = crpitos.get(name = 'Bitcoin')
                if float(crpito.valor)*float(monto) < user.USD_Count:
                    if int(accion) == 0:
                        user.BTC_Count += float(monto) 
                        if email_emis != 'null':
                            user_emi.USD_Count -= float(crpito.valor)*float(monto)
                    else:
                        user.BTC_Count -= float(monto)
                        if email_emis != 'null':
                            user_emi.USD_Count += float(crpito.valor)*float(monto)
                else:
                    return 'Dinero insuficiente, compre dolares!'
            elif int(moneda) == 1:#-------------------------------------------------------------------------------------
                crpito = crpitos.get(name = 'XRP')
                if float(crpito.valor)*float(monto) < user.USD_Count:
                    if int(accion) == 0:
                        user.XRP_Count += float(monto)
                        if email_emis != 'null':
                            user_emi.USD_Count -= float(crpito.valor)*float(monto)
                    else:
                        user.XRP_Count -= float(monto)
                        if email_emis != 'null':
                            user_emi.USD_Count += float(crpito.valor)*float(monto)
                else:
                    return 'Dinero insuficiente, compre dolares!'
            elif int(moneda) == 2:#-------------------------------------------------------------------------------------
                crpito = crpitos.get(name = 'Dogecoin')
                
                if float(crpito.valor)*float(monto) < user.USD_Count:
                    if int(accion) == 0:
                        user.DOGE_Count += float(monto)
                        if email_emis != 'null':
                            user_emi.USD_Count -= float(crpito.valor)*float(monto)
                    else:
                        user.DOGE_Count -= float(monto)
                        if email_emis != 'null':
                            user_emi.USD_Count += float(crpito.valor)*float(monto)
                else:
                    return 'Dinero insuficiente, compre dolares!'
            elif int(moneda) == 3:#-------------------------------------------------------------------------------------
                if int(accion) == 0:
                    user.USD_Count += float(monto)
                else:
                    user.USD_Count -= float(monto)
            user.save()
            return ('Transaccion realizada con exito')
        
    except :    
        e = sys.exc_info()[1]
        return(  e )
        # return ()
    
#BuySell se encarga las acciones de comprar y vender criptos o USD
def buySell (request):

    
    data = {
        'form': CommerForm()
    }

    #Modifico el form para poder guardarlo correctamente en la BBDD
    if request.method == 'POST':
        request.POST._mutable = True
        request.POST['email'] = User.email
        request.POST.pop('csrfmiddlewaretoken')
        request.POST._mutable = False 
        formulario =  CommerForm(data= request.POST)

        #Si el formulario es valido, llamo a la funcion CoinOperations para que haga la transferencia
        if formulario.is_valid():
            CoinOperations(
                moneda= request.POST['moneda'],
                accion= request.POST['accion'],
                monto= request.POST['monto'],
                email= request.POST['email'],
                email_emis= request.POST['email'])
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