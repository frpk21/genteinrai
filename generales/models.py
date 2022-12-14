import os
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
#from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver


class ClaseModelo(models.Model):
    activo = models.BooleanField(default=True, null=True)
    creado = models.DateTimeField(auto_now_add=True, null=True)
    modificado = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract=True

from generales.models import ClaseModelo

class Sedes(ClaseModelo):
    sede = models.IntegerField(default=0, null=False, blank=False)
    nombre_sede = models.CharField(blank=False, null=False, max_length=100, default="")
    foto = models.FileField("Foto Sede (476x570)", upload_to="fotos/", blank=False, null=False, default="")
    foto1 = models.FileField("Foto Sede (1170x610)", upload_to="fotos/", blank=True, null=True, default="")
    foto2 = models.FileField("Foto Sede (1170x610)", upload_to="fotos/", blank=True, null=True, default="")
    foto3 = models.FileField("Foto Sede (1170x610)", upload_to="fotos/", blank=True, null=True, default="")
    director = models.CharField(blank=True, null=True, max_length=100, default="")
    ciudad = models.CharField(blank=True, null=True, max_length=50, default="")
    ano_fundacion = models.IntegerField(default=0, null=True, blank=True)
    direccion = models.CharField(blank=True, null=True, max_length=100, default="")
    logo = models.FileField("Logo (476x570)", upload_to="fotos/", blank=False, null=False, default="")
    descripcion = RichTextField(max_length=15000, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.nombre_sede)

    def save(self):
        self.nombre_sede = self.nombre_sede.upper()
        self.director = self.director.upper()
        self.ciudad = self.ciudad.upper()
        super(Sedes, self).save()

    class Meta:
        verbose_name_plural = "Sedes"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.FileField("Archivo con Foto del Usuario", upload_to="fotos/", blank=False, null=False, default="")
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=0, null=False, blank=False)
 
    def save(self):
        super(Profile, self).save()

    class Meta:
        verbose_name_plural = "Perfiles de Usuarios"

class Cargos(models.Model):
    nombre = models.CharField('Nombre Cargo', default='', blank=True, null=True, max_length=100)
 
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Cargos, self).save()

    class Meta:
        verbose_name_plural = "Cargos de Funcionarios"

class Funcionarios(models.Model):
    nombre1 = models.CharField('Primer nombre', default='', blank=False, null=False, max_length=50)
    nombre2 = models.CharField('Segundo nombre', default='', blank=True, null=True, max_length=50)
    apellido1 = models.CharField('Primer apellido', default='', blank=False, null=False, max_length=50)
    apellido2 = models.CharField('Segundo apellido', default='', blank=True, null=True, max_length=50)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', blank=False, null=False)
    foto = models.FileField("Archivo con Foto del Funcionario (200 x 200px)", upload_to="fotos/", blank=False, null=False, default="")
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=0, null=False, blank=False)
    direccion = models.CharField('Direcci??n Residencia', default='', blank=True, null=True, max_length=100)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE, default=0, null=False, blank=False)
    celular = models.CharField('N??mero de celular', default='', blank=True, null=True, max_length=60)
    email = models.CharField('E-Mail', blank=True, null=True, max_length=200, default="" )

    def __str__(self):
        return '{} {} {} {}'.format(self.nombre1, self.nombre2, self.apellido1, self.apellido2)
 
    def save(self):
        self.nombre1 = self.nombre1.upper()
        self.nombre2 = self.nombre2.upper()
        self.apellido1 = self.apellido1.upper()
        self.apellido2 = self.apellido2.upper()
        super(Funcionarios, self).save()

class Noticias(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    subtitulo = models.CharField(blank=False, null=False, max_length=500)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    urlvideo = models.CharField('URL Youtube', blank=True, null=True, default='', max_length=200)
    ultima_hora = models.BooleanField()
    evento = models.BooleanField(default='False')
    fecha_inicio_publicacion = models.DateField('Fecha de inicio de publicaci??n', blank=True, null=True, default=datetime.now)
    fecha_final_publicacion = models.DateField('Fecha de finalizaci??n de publicaci??n', blank=True, null=True, default=datetime.now)
    CHOICES = ((0,'Principal'),(1,'Destacado 1'),(2,'Destacado 2'),(3,'Destacado 3'),(4,'General 4'))
    orden_destacado = models.IntegerField(choices=CHOICES, default=0, blank=False, null=False)
    imagen_destacado = models.FileField("Imagen Destacado (476 x 570px)", upload_to="imagenes/", blank=True, null=True)
    inrai_video = models.TextField("Video Streaming Inrai",max_length=10000, default="", blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')
    fuente = models.CharField(help_text='Fuente noticia', blank=False, null=False, max_length=50, default="INRAI")
    html = models.TextField(max_length=10000, default="", blank=True, null=True)
    pdf = models.FileField("Archivo PDF", upload_to="pdf/", blank=True, null=True, default='')
    slug = models.SlugField(blank=True,null=True, max_length=250)
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=0, null=False, blank=False)

    def __str__(self):
        return '{}-{}'.format(self.titulo, self.autor.profile.sede.nombre_sede)

    def save(self):
        self.slug = slugify(self.titulo)
        super(Noticias, self).save()

    class Meta:
        verbose_name_plural = "Noticias"


class Suscribir(ClaseModelo):
    email = models.CharField(max_length=200, help_text='eMail', unique=True)

    def __str__(self):
        return '{}'.format(self.email)

    class Meta:
        verbose_name_plural = "Suscribirse"


class Miempresa(models.Model):
    nuestra_empresa = RichTextField("Nuestra Empresa", max_length=15000, blank=True, null=True)
    mision = RichTextField("Mision", max_length=15000, blank=True, null=True)
    vision = RichTextField("Vision", max_length=15000, blank=True, null=True)
    objetivo = RichTextField("Objetivo General", max_length=15000, blank=True, null=True)
    principios = RichTextField("Principios y Fundamentos", max_length=15000, blank=True, null=True)
    himno_letra = RichTextField("Letra Himno Sistema INRAI", max_length=15000, blank=True, null=True)
    himno_audio = models.FileField("Archivo Audio Himno Sistema INRAI", upload_to="audio/", blank=True, null=True, default='')
 
    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name_plural = "Nuestra Empresa"

class Home1(models.Model):
    nuestra_empresa = RichTextField("Nuestra Empresa", max_length=3000, blank=True, null=True)
    comunicaciones = RichTextField("Comunicaciones", max_length=3000, blank=True, null=True)
    marketing = RichTextField("Marketing", max_length=3000, blank=True, null=True)
    entretenimiento = RichTextField("Entretenimiento", max_length=3000, blank=True, null=True)
   
    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name_plural = "Home"

class Bienestar(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    detalle = RichTextField("Detalle", max_length=15000, blank=True, null=True)
    foto = models.FileField("Foto (417 x 269px)", upload_to="fotos/", blank=True, null=True, default='')
    CHOICES = (('news','Noticias'),('event','Eventos'),('insp','Medio Ambiente'))
    tipo = models.CharField(choices=CHOICES, max_length=5, default='news', blank=False, null=False)
 
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.titulo = self.titulo.upper()
        super(Bienestar, self).save()

    class Meta:
        verbose_name_plural = "Bienestar Social"



class Tipos_tutoriales(ClaseModelo):
    nombre = models.CharField(blank=False, null=False, max_length=200)
 
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self):
        self.nombre = self.nombre.upper()
        super(Tipos_tutoriales, self).save()

    class Meta:
        verbose_name_plural = "Temas de Tutoriales"


class Tutoriales(ClaseModelo):
    tipo = models.ForeignKey(Tipos_tutoriales, on_delete=models.CASCADE, default=0, null=False, blank=False)
    titulo = models.CharField(blank=False, null=False, max_length=200)
    subtitulo = models.CharField(blank=False, null=False, max_length=500)
    urlvideo = models.CharField('URL Youtube', blank=True, null=True, default='', max_length=200)
    archivo_video = models.FileField("Archivo de Video", upload_to="tutoriales/", blank=True, null=True, default='')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')

    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.titulo = self.titulo.upper()
        super(Tutoriales, self).save()

    class Meta:
        verbose_name_plural = "Tutoriales"


class Ocupacional(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    detalle = RichTextField("Detalle", max_length=15000, blank=True, null=True)
    foto = models.FileField("Foto (417 x 269px)", upload_to="fotos/", blank=True, null=True, default='')
 
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.titulo = self.titulo.upper()
        super(Ocupacional, self).save()

    class Meta:
        verbose_name_plural = "Salud Ocupacional"


class Elmuro(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    detalle = RichTextField("Detalle", max_length=5000, blank=True, null=True)
    foto = models.FileField("Foto (417 x 269px)", upload_to="elmuro/", blank=True, null=True, default='')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')
 
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self):
        self.slug = slugify(self.titulo)
        super(Elmuro, self).save()

    class Meta:
        verbose_name_plural = "El Muro"


class Reglamento(models.Model):
    reglamento = RichTextField("Reglamento Interno de Trabajo", max_length=200000, blank=True, null=True)
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=1, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.sede.nombre_sede)

    class Meta:
        verbose_name_plural = "Reglamento"        