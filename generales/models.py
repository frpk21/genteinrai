import os
from django.db import models
from django.template.defaultfilters import slugify
from django_ckeditor_5.fields import CKEditor5Field

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
    descripcion = CKEditor5Field(max_length=15000, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.nombre_sede)

    def save(self, *args, **kwargs):
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
 
    def save(self, *args, **kwargs):
        super(Profile, self).save()

    class Meta:
        verbose_name_plural = "Perfiles de Usuarios"

class Cargos(models.Model):
    nombre = models.CharField('Nombre Cargo', default='', blank=True, null=True, max_length=100)
 
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Cargos, self).save()

    class Meta:
        verbose_name_plural = "Cargos de Funcionarios"

class Funcionarios(models.Model):
    nombre1 = models.CharField('Primer nombre', default='', blank=False, null=False, max_length=50)
    nombre2 = models.CharField('Segundo nombre', default='', blank=True, null=True, max_length=50)
    apellido1 = models.CharField('Primer apellido', default='', blank=False, null=False, max_length=50)
    apellido2 = models.CharField('Segundo apellido', default='', blank=True, null=True, max_length=50)
    cedula = models.CharField('Cédula No. (ID) ', default='', blank=False, null=False, max_length=50)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', blank=False, null=False)
    foto = models.FileField("Archivo con Foto del Funcionario (250 x 250px  FONDO BLANCO)", upload_to="fotos/", blank=False, null=False, default="")
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=0, null=False, blank=False)
    direccion = models.CharField('Dirección Residencia', default='', blank=True, null=True, max_length=100)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE, default=0, null=False, blank=False)
    celular = models.CharField('Número de celular', default='', blank=True, null=True, max_length=60)
    email = models.CharField('E-Mail', blank=True, null=True, max_length=200, default="" )
    CHOICES = ((0,'Indefinido'),(1,'Fijo'), (2, 'Aprendiz SENA'))
    tipo_contrato = models.IntegerField(choices=CHOICES, default=0, null=False, blank=False)
    fecha_inicio = models.DateField('Fecha de inicio de labores', blank=False, null=False)
    fecha_ultimo_carnet = models.DateField('Fecha de emisión del último carnet', blank=True, null=False)
    hora_entrada = models.TimeField('Hora de entrada (inicio jornada)', default='07:00', blank=False, null=False)
    hora_salida_almuerzo = models.TimeField('Hora de salida almuerzo', default='12:00', blank=True, null=False)
    hora_entrada_de_almuerzo = models.TimeField('Hora entrada de almuerzo', default='14:00', blank=True, null=False)
    hora_salida = models.TimeField('Hora salida (terminación jornada)',  default='18:00',blank=False, null=False)
    CHOICES1 = ((0,'Ausente'),(1,'En Oficina'))
    estado = models.IntegerField(choices=CHOICES1, default=0, null=False, blank=False)

    def __str__(self):
        return '{} {} {} {}'.format(self.nombre1, self.nombre2, self.apellido1, self.apellido2)
 
    def save(self, *args, **kwargs):
        self.nombre1 = self.nombre1.upper()
        if self.nombre2:
            self.nombre2 = self.nombre2.upper()
        self.apellido1 = self.apellido1.upper()
        self.apellido2 = self.apellido2.upper()
        super(Funcionarios, self).save()

    class Meta:
        verbose_name_plural = "Funcionarios"


# Refactor: Control eficiente de eventos de asistencia
class io_funcionarios(models.Model):
    EVENTO_ENTRADA = 0
    EVENTO_SALIDA = 1
    EVENTO_INICIO_ALMUERZO = 2
    EVENTO_FIN_ALMUERZO = 3
    EVENTO_OTRO = 4
    EVENTO_CHOICES = (
        (EVENTO_ENTRADA, 'Entrada'),
        (EVENTO_SALIDA, 'Salida'),
        (EVENTO_INICIO_ALMUERZO, 'Inicio Almuerzo'),
        (EVENTO_FIN_ALMUERZO, 'Fin Almuerzo'),
        (EVENTO_OTRO, 'Otro'),
    )
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.CASCADE, null=False, blank=False)
    fecha = models.DateField('Fecha', blank=False, null=False)
    hora = models.TimeField('Hora', blank=False, null=False)
    tipo_evento = models.IntegerField(choices=EVENTO_CHOICES, default=EVENTO_ENTRADA, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Eventos de Asistencia"
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.funcionario} - {self.get_tipo_evento_display()} - {self.fecha} {self.hora}"

    @staticmethod
    def eventos_del_dia(funcionario, fecha):
        return io_funcionarios.objects.filter(funcionario=funcionario, fecha=fecha).order_by('hora')

    @staticmethod
    def resumen_jornada(funcionario, fecha):
        eventos = list(io_funcionarios.eventos_del_dia(funcionario, fecha))
        resumen = {
            'entrada': None,
            'salida': None,
            'inicio_almuerzo': None,
            'fin_almuerzo': None,
            'otros': [],
        }
        for e in eventos:
            if e.tipo_evento == io_funcionarios.EVENTO_ENTRADA:
                resumen['entrada'] = e.hora
            elif e.tipo_evento == io_funcionarios.EVENTO_SALIDA:
                resumen['salida'] = e.hora
            elif e.tipo_evento == io_funcionarios.EVENTO_INICIO_ALMUERZO:
                resumen['inicio_almuerzo'] = e.hora
            elif e.tipo_evento == io_funcionarios.EVENTO_FIN_ALMUERZO:
                resumen['fin_almuerzo'] = e.hora
            else:
                resumen['otros'].append(e.hora)
        return resumen

    @staticmethod
    def calcular_estado_asistencia(funcionario, fecha):
        """Resumen del cumplimiento de jornada para un funcionario en una fecha.

        Devuelve un dict con:
            presente, retardo, salida_anticipada, ausente,
            horas_trabajadas (neto, descontando almuerzo si está registrado),
            minutos_retardo, minutos_salida_anticipada.
        """
        from datetime import datetime as _dt, timedelta as _td

        jornada = io_funcionarios.resumen_jornada(funcionario, fecha)
        estado = {
            'presente': bool(jornada['entrada'] and jornada['salida']),
            'retardo': False,
            'salida_anticipada': False,
            'ausente': False,
            'horas_trabajadas': None,
            'minutos_retardo': 0,
            'minutos_salida_anticipada': 0,
        }

        if not jornada['entrada'] and not jornada['salida']:
            estado['ausente'] = True
            return estado

        if jornada['entrada'] and funcionario.hora_entrada and jornada['entrada'] > funcionario.hora_entrada:
            estado['retardo'] = True
            dt_esp = _dt.combine(fecha, funcionario.hora_entrada)
            dt_real = _dt.combine(fecha, jornada['entrada'])
            estado['minutos_retardo'] = int((dt_real - dt_esp).total_seconds() // 60)

        if jornada['salida'] and funcionario.hora_salida and jornada['salida'] < funcionario.hora_salida:
            estado['salida_anticipada'] = True
            dt_esp = _dt.combine(fecha, funcionario.hora_salida)
            dt_real = _dt.combine(fecha, jornada['salida'])
            estado['minutos_salida_anticipada'] = int((dt_esp - dt_real).total_seconds() // 60)

        if jornada['entrada'] and jornada['salida']:
            dt_entrada = _dt.combine(fecha, jornada['entrada'])
            dt_salida = _dt.combine(fecha, jornada['salida'])
            if dt_salida < dt_entrada:
                # Caso turno que cruza medianoche: sumar un día a la salida.
                dt_salida += _td(days=1)
            delta = dt_salida - dt_entrada

            # Descontar almuerzo si ambos extremos están registrados.
            if jornada['inicio_almuerzo'] and jornada['fin_almuerzo']:
                dt_ini_alm = _dt.combine(fecha, jornada['inicio_almuerzo'])
                dt_fin_alm = _dt.combine(fecha, jornada['fin_almuerzo'])
                if dt_fin_alm > dt_ini_alm:
                    delta -= (dt_fin_alm - dt_ini_alm)

            estado['horas_trabajadas'] = round(delta.total_seconds() / 3600.0, 2)

        return estado

class Noticias(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    subtitulo = models.CharField(blank=False, null=False, max_length=500)
    descripcion = CKEditor5Field(max_length=15000, blank=True, null=True)
    archivo_audio = models.FileField("Archivo Audio", upload_to="audio/", blank=True, null=True, default='')
    urlvideo = models.CharField('URL Youtube', blank=True, null=True, default='', max_length=200)
    ultima_hora = models.BooleanField()
    evento = models.BooleanField(default='False')
    fecha_inicio_publicacion = models.DateField('Fecha de inicio de publicación', blank=True, null=True, default=datetime.now)
    fecha_final_publicacion = models.DateField('Fecha de finalización de publicación', blank=True, null=True, default=datetime.now)
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

    def save(self, *args, **kwargs):
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
    nuestra_empresa = CKEditor5Field("Nuestra Empresa", max_length=15000, blank=True, null=True)
    mision = CKEditor5Field("Mision", max_length=15000, blank=True, null=True)
    vision = CKEditor5Field("Vision", max_length=15000, blank=True, null=True)
    objetivo = CKEditor5Field("Objetivo General", max_length=15000, blank=True, null=True)
    principios = CKEditor5Field("Principios y Fundamentos", max_length=15000, blank=True, null=True)
    himno_letra = CKEditor5Field("Letra Himno Sistema INRAI", max_length=15000, blank=True, null=True)
    himno_audio = models.FileField("Archivo Audio Himno Sistema INRAI", upload_to="audio/", blank=True, null=True, default='')
 
    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name_plural = "Nuestra Empresa"

class Home1(models.Model):
    nuestra_empresa = CKEditor5Field("Nuestra Empresa", max_length=3000, blank=True, null=True)
    comunicaciones = CKEditor5Field("Comunicaciones", max_length=3000, blank=True, null=True)
    marketing = CKEditor5Field("Marketing", max_length=3000, blank=True, null=True)
    entretenimiento = CKEditor5Field("Entretenimiento", max_length=3000, blank=True, null=True)
   
    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        verbose_name_plural = "Home"

class Bienestar(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    detalle = CKEditor5Field("Detalle", max_length=15000, blank=True, null=True)
    foto = models.FileField("Foto (417 x 269px)", upload_to="fotos/", blank=True, null=True, default='')
    CHOICES = (('news','Noticias'),('event','Eventos'),('insp','Medio Ambiente'))
    tipo = models.CharField(choices=CHOICES, max_length=5, default='news', blank=False, null=False)
 
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self, *args, **kwargs):
        self.titulo = self.titulo.upper()
        super(Bienestar, self).save()

    class Meta:
        verbose_name_plural = "Bienestar Social"



class Tipos_tutoriales(ClaseModelo):
    nombre = models.CharField(blank=False, null=False, max_length=200)
 
    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
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

    def save(self, *args, **kwargs):
        self.titulo = self.titulo.upper()
        super(Tutoriales, self).save()

    class Meta:
        verbose_name_plural = "Tutoriales"


class Ocupacional(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    detalle = CKEditor5Field("Detalle", max_length=15000, blank=True, null=True)
    foto = models.FileField("Foto (417 x 269px)", upload_to="fotos/", blank=True, null=True, default='')
 
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self, *args, **kwargs):
        self.titulo = self.titulo.upper()
        super(Ocupacional, self).save()

    class Meta:
        verbose_name_plural = "Salud Ocupacional"


class Elmuro(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    detalle = CKEditor5Field("Detalle", max_length=5000, blank=True, null=True)
    foto = models.FileField("Foto (417 x 269px)", upload_to="elmuro/", blank=True, null=True, default='')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,default='')
 
    def __str__(self):
        return '{}'.format(self.titulo)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Elmuro, self).save()

    class Meta:
        verbose_name_plural = "El Muro"


class Reglamento(models.Model):
    reglamento = CKEditor5Field("Reglamento Interno de Trabajo", max_length=200000, blank=True, null=True)
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=1, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.sede.nombre_sede)

    class Meta:
        verbose_name_plural = "Reglamento"
