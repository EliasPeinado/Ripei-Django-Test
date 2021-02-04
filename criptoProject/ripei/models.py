from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator



class UserProfileManager(BaseUserManager):
    def create_user(self, name, email, password = None):
        if not email:
            raise('el usuario debe tener un email')

        email = self.normalize_email(email)
        user = self.model(email=email, name = name)
        user.set_password(password)
        user.save(using = self._db)

        return user
    
    def create_superuser(self,name, email, password):
        user = self.create_user(email, name, password)
        is_superuser =True
        is_staff = True
        user.save(using = self._db)




class UserProfile(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)


    isActive = models.BooleanField(default=True)
    is_Staff = models.BooleanField(default=False)
    BTC_Count = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de Bitcoin ')
    XRP_Count = models.FloatField(default=10, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de XRP ')
    DOGE_Count = models.FloatField(default=10, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de Dogecoin')
    USD_Count = models.PositiveIntegerField(default=100000, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de Dolares Americanos')


    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] 

    def __str__ (self):
        return self.email

    




class Crito(models.Model):
    name = models.CharField(max_length=50)
    valor = models.FloatField(validators=[MinValueValidator(0)])
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to = 'products', null = True)

    def __str__(self):
        return self.name

opciones_consulta = [
    [0,'consulta'],
    [1,'reclamo'],
    [2,'sugerencia'],
    [3,'felicitaciones']
]

class Contacto(models.Model):

    
    nombre = models.CharField(max_length=50)
    corre = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consulta) 
    mensaje = models.TextField()
    avisos = models.BooleanField() 

    def __str__(self):
        return self.nombre

monedas = [
    [0, 'Bitcoin'],
    [1, 'XRP'],
    [2, 'Dogecoin'],
    [3, 'USD']
]
class Historial_Transfer (models.Model):
    receptor_email = models.EmailField(max_length= 100)
    receptor_name = models.CharField(max_length= 100)
    emisor_email = models.EmailField(max_length= 100)
    emisor_name = models.CharField(max_length= 100)
    monto = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    moneda =  models.IntegerField(choices=monedas,  default=monedas[2] )

acciones = [
    [0, 'Comoprar'],
    [1, 'Vender']
]

class Historial_Commer (models.Model):
    email = models.EmailField(max_length= 100)
    monto = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    moneda =  models.IntegerField(choices=monedas,  default=monedas[2])
    accion = models.IntegerField(choices=acciones, default=acciones[0])
    