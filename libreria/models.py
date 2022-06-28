from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from requests import request

# Create your models here.
class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        	return self.nombre
	

class Usuario(AbstractUser):
    # atributos adicionales.
    email = models.EmailField('email address', unique = True)
    ciudad = models.ForeignKey(to=Ciudad ,on_delete=models.CASCADE, default=1)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'ciudad']

class Idioma(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
        	return self.nombre


class Genero(models.Model):
	nombre = models.CharField(max_length=255)
	
	def __str__(self):
        	return self.nombre

class Editorial(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
        	return self.nombre

	
class Tipo(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
        	return self.nombre


class Articulo(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.IntegerField()
    stock = models.IntegerField()
    genero = models.ManyToManyField(Genero)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)

	
    def __str__(self):
        return self.nombre
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class Compra(models.Model):
	fecha = models.DateField()
	precio_total = models.IntegerField()
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class Ejemplar(models.Model):
	articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)


