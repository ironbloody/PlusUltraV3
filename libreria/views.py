from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pyparsing import autoname_elements
from django.contrib import messages

from libreria.carrito import Carrito

from .models import Articulo, Tipo, Usuario
from .forms import ArticuloForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth.models import Group 

from django.http import FileResponse
import csv
import io
from reportlab.pdfgen import canvas

# Create your views here.
def Registro(request):
        if request.user.is_authenticated:
                return redirect('inicio')
        else:
                form = RegisterForm()
                if request.method == 'POST':
                        form = RegisterForm(request.POST)
                        if form.is_valid():
                                form.save()
                                user = form.cleaned_data.get('username')
                                messages.success(request, 'Se crea la cuenta exitosamente para el usuario ' + user)
                                return redirect('login')
			
                context = {'form':form}
        return render(request, 'paginas/registro.html', context)

def Login(request):
        if request.user.is_authenticated:
                return redirect('inicio')
        else:
                if request.method == 'POST':
                        username = request.POST.get('username')
                        password =request.POST.get('password')

                        user = authenticate(request, username=username, password=password)

                        if user is not None:
                                        login(request, user)
                                        return redirect('inicio')
                        else:
                                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'paginas/login.html')
def Logout(request):
        logout(request)
        messages.success(request, 'Yor Were logged out')
        return redirect('inicio')

def inicio(request):
        return render(request, 'paginas/inicio.html')

def home(request): 
        return render(request, 'paginas/home.html')

def libros(request): 
        libros = Articulo.objects.filter(tipo = 1)
        return render(request, 'libros/libros.html', {'libros': libros})
def mangas(request): 
        mangas = Articulo.objects.filter(tipo = 3)
        return render(request, 'libros/mangas.html', {'mangas': mangas})

def comics(request): 
        comics = Articulo.objects.filter(tipo = 4)
        return render(request, 'libros/comics.html', {'comics': comics})

def crear_libro(request):
        formulario = ArticuloForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
                formulario.save()
                return redirect('libros')

        return render(request, 'libros/crear_libro.html', {'formulario': formulario})

def crear_manga(request):
        formulario = ArticuloForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
                formulario.save()
                return redirect('mangas')

        return render(request, 'libros/crear_manga.html', {'formulario': formulario})

def crear_comic(request):
        formulario = ArticuloForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
                formulario.save()
                return redirect('comics')

        return render(request, 'libros/crear_comic.html', {'formulario': formulario})
        
def editar(request, id):
        libro = Articulo.objects.get(id=id)
        formulario = ArticuloForm(request.POST or None, request.FILES or None, instance=libro)
        if formulario.is_valid() and request.POST:
                formulario.save()
                return redirect('libros')
        return render(request, 'libros/editar.html', {'formulario': formulario})

def eliminar(request, id):
        libro = Articulo.objects.get(id=id)
        libro.delete()
        return render('libros')

def agregar_articulo(request, id):
        carrito = Carrito(request)
        libro = Articulo.objects.get(id=id)
        carrito.agregar(libro)
        return redirect("libros")

def eliminar_articulo(request, id):
        carrito = Carrito(request)
        libro = Articulo.objects.get(id=id)
        carrito.eliminar(libro)
        return redirect("libros")

def restar_articulo(request, id):
        carrito = Carrito(request)
        libro = Articulo.objects.get(id=id)
        carrito.restar(libro)
        return redirect("libros")

def limpiar_carrito(request):
        carrito = Carrito(request)
        carrito.limpiar()
        return redirect("libros")


register = template.Library() 

# Para exportar un CSV, el cual obtiene de los articulos el nombre, precio y el stock
def article_list(request):
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="Articulos.csv"'  
    queryset = Articulo.objects.all()
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Precio', 'Stock'])
    for article in queryset:  
        writer.writerow([article.nombre, article.precio, article.stock])  
    return response 

# Acá es donde se crea el PDF de ver el horario
def horario(request):
    buffer = io.BytesIO()
    x = canvas.Canvas(buffer)
    x.drawString(200, 800, "Horarios de disponibilidad Local PlusUltra")
    x.drawString(10, 750, "Lunes a viernes: 11:00 - 14:00 y 15:00 - 19:00")
    x.drawString(10, 700, "Sabado: 11:00 - 14:00 y 15:00 - 18:00")
    x.drawString(10, 650, "Plataforma de atención:")
    x.drawString(10, 600, "Instagram: @plusultralibreria")

    x.showPage()
    x.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Horario_e_informacion.pdf')

def grafico(request):
    labels = []
    data = []
    queryset = Articulo.objects.order_by('tipo')[:5]
    for article in queryset:
        labels.append(article.nombre)
        data.append(article.stock)
    return render(request, 'paginas/grafico.html', {'labels': labels, 'data': data,})
@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
