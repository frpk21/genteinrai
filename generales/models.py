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

class io_funcionarios(models.Model):
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.CASCADE, default=0, null=False, blank=False)
    fecha = models.DateField('Fecha de nacimiento', blank=False, null=False)
    hora = models.TimeField(blank=True, null=False)
    CHOICES = ((0,'Entra'),(1,'Sale'))
    tipo_evento = models.IntegerField(choices=CHOICES, default=0, null=False, blank=False)

    class Meta:
        verbose_name_plural = "IO Funcionarios"

class Noticias(ClaseModelo):
    titulo = models.CharField(blank=False, null=False, max_length=200)
    subtitulo = models.CharField(blank=False, null=False, max_length=500)
    descripcion = RichTextField(max_length=15000, blank=True, null=True)
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
    detalle = RichTextField("Detalle", max_length=15000, blank=True, null=True)
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
    detalle = RichTextField("Detalle", max_length=5000, blank=True, null=True)
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
    reglamento = RichTextField("Reglamento Interno de Trabajo", max_length=200000, blank=True, null=True)
    sede = models.ForeignKey(Sedes, on_delete=models.CASCADE, default=1, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.sede.nombre_sede)

    class Meta:
        verbose_name_plural = "Reglamento"

def reporte_diario(request):
        import io
        from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib import colors  
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import Table
        from reportlab.lib.units import inch
        from reportlab.platypus import Image, Paragraph, Spacer
        from django.core.mail import EmailMessage
        from django.http import HttpResponse

        response = HttpResponse(content_type='application/pdf')  
        buffer = io.BytesIO()
        ordenes = []
        logo = "static/base/img/inrai/logo-inrai-300px.png"
        texto = "static/base/img/inrai/logo-inrai-300px.png"
        image = Image(logo, 3 * inch, 1.2 * inch)
        image.hAlign = "LEFT"
        image1 = Image(texto, 2 * inch, 0.5 * inch)
        image1.hAlign = "LEFT"
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Normal_CENTER', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='obs_imp', alignment=TA_LEFT,fontSize=10 ))
        styles.add(ParagraphStyle(name='Pie',
                            alignment=TA_CENTER,
                            fontName='Helvetica',
                            fontSize=14,
                            textColor=colors.darkgray,
                            leading=8,
                            textTransform='uppercase',
                            wordWrap='LTR',
                            splitLongWords=True,
                            spaceShrinkage=0.05,
                            ))
        styles.add(ParagraphStyle(name='link',
                            alignment=TA_CENTER,
                            fontName='Helvetica',
                            fontSize=12,
                            textColor=colors.blue,
                            leading=8,
                            textTransform='lowercase',
                            wordWrap='LTR',
                            splitLongWords=False,
                            spaceShrinkage=0,
                            #backColor=colors.cyan,
                            ))
        styles.add(ParagraphStyle(name='confirma',
                            alignment=TA_CENTER,
                            fontName='Helvetica',
                            fontSize=10,
                            textColor=colors.red,
                            leading=8,
                            #textTransform='lowercase',
                            wordWrap='LTR',
                            splitLongWords=False,
                            spaceAfter=3,
                            spaceBefore=3,
                            spaceShrinkage=0,
                            backColor=colors.yellow,
                            ))
        styles.add(ParagraphStyle(name='ejemplo',
                            parent=styles['Normal'],
                            fontName='Helvetica',
                            wordWrap='LTR',
                            alignment=TA_LEFT,
                            fontSize=12,
                            leading=13,
                            textColor=colors.red,
                            borderPadding=0,
                            leftIndent=0,
                            backcolor=colors.yellow,
                            rightIndent=0,
                            spaceAfter=0,
                            spaceBefore=0,
                            splitLongWords=True,
                            spaceShrinkage=0.05,
                            ))
        styles.add(ParagraphStyle(name='ejemplo1',
                            parent=styles['Normal'],
                            fontName='Helvetica',
                            wordWrap='LTR',
                            alignment=TA_CENTER,
                            fontSize=12,
                            leading=13,
                            textColor=colors.red,
                            borderPadding=1,
                            leftIndent=0,
                            backcolor=colors.yellow,
                            rightIndent=0,
                            spaceAfter=0,
                            spaceBefore=2,
                            splitLongWords=True,
                            spaceShrinkage=0.05,
                            ))
        tit="         Rad-No. "
        filename = "Reporte_horarios.pdf"
        
        t=Table(
            data=[
                [image1,'','',''],
                ['','','',''],
                ['REPORTE HORARIOS DE PERSONAL','','',''],
                ['','','',''],
                ['FECHA', '',(date.today()-1).strftime('%d/%m/%Y')+tit,'',''],
                ['', '','',''],
                ['', '','',''],
                ['', '','',''],
                ['', '','',''],
                ['', '','','']
            ],
            colWidths=[70,20,350,200],
            style=[
                    ("FONT", (0,0), (0,2), "Helvetica-Bold", 15, 15,colors.grey),
                    ("FONT", (1,0), (5,1), "Helvetica", 7, 7,colors.grey),
                    ("FONT", (1,2), (2,-1), "Helvetica-Bold", 11, 11),
                ]
            )
        
        t.hAlign = "LEFT"
        ordenes.append(t)
        ordenes.append(Spacer(1, 5))
        try:
            nube=self.open_db_cloud()
            cursor_nube=nube.cursor()
            try:
                cursor_nube.execute("SELECT * FROM generales_sedes")
                sedes = namedtuplefetchall(cursor_nube)
                for n, x in enumerate(sedes):
                    sql="SELECT generales_funcionarios.nombre1 as n1, generales_funcionarios.nombre2 as n2, generales_funcionarios.apellido1 as a1, generales_funcionarios.apellido2 as a2, generales_funcionarios.hora_entrada as h1, generales_funcionarios.hora_salida as h2"
                    sql = sql + " generales_io_funcionarios.fecha, generales_io_funcionarios.hora, generales_io_funcionarios.tipo_evento"
                    sql = sql + " FROM generales_io_funcionarios LEFT JOIN generales_funcionarios on generales_io_funcionarios.id=funcionarios.id where generales_funcionarios.sede_id="+str(x.id).strip()+" AND fecha=(current_date-1)"
                    cursor_nube.execute(sql)
                    resul = namedtuplefetchall(cursor_nube)
                    if resul:
                        for i,p in enumerate(resul):
                            ordenes0= [(p.n1 + p.n2 + p.a1 + p.a2,
                                        p.feha_entrada+" - "+p.fecha_salida,
                                        p.fecha,
                                        p.hora,
                                        p.tipo_evento)]
                        headings0 = ('Funcionario', 'Horario', 'Fecha', 'Hora', 'Evento')
                        col = 5
            except psycopg2.Error as e:
                self.lbl_error.setText("ERROR DE CONEXION SERVIDOR VIRTUAL: "+str(e))
                self.lbl_error.show()
            cursor_nube.close()
            nube.close()
        except psycopg2.Error as e:
            self.lbl_error.setText("SERVIDOR VIRTUAL: "+datetime.now().strftime('%d/%m/%Y %H:%M')+" *** ERROR DE CONEXION SV EN LA NUBE *** "+str(e))
            self.lbl_error.show()                
            t0 = Table([headings0] + ordenes0)
            t0.setStyle(TableStyle(
                [  
                    ('GRID', (0, 0), (col, -1), 1, colors.darkgray),  
                    #('LINEBELOW', (0, 0), (-1, 0), 2, colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN',(0,1),(col,1),'CENTRE'),
                    ('BACKGROUND', (0, 0), (col,0), colors.gray)  
                ]  
            ))
            t0.hAlign = "LEFT"
            ordenes.append(t0)
        ordenes.append(Spacer(10, 15))
        pie = Paragraph("inrai.net", styles['Pie'])
        pie.hAlign = "CENTER"
        ordenes.append(pie)
        icon = "static/base/img/inrai/favicon.png"
        
        doc = SimpleDocTemplate(buffer,
                    pagesize=landscape(letter),
                    rightMargin=40,
                    leftMargin=50,
                    topMargin=20,  
                    bottomMargin=8,
                    author="INRAI",
                    title="REPORTE DE HORARIOS DEL PERSONAL",
                    icon=icon,
                    )
        
        doc.build(ordenes)
        response.write(buffer.getvalue())
        pdf = buffer.getvalue()
        buffer.close()

        return response
