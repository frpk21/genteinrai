from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from genteinrai import settings
from datetime import date
from django.shortcuts import redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.list import ListView
from django.shortcuts import render
from django.db import connections
from collections import namedtuple
from django.http import JsonResponse
from datetime import datetime, timedelta
from generales.forms import MesAnoForm
from .models import Bienestar, Noticias, Ocupacional, Sedes, Miempresa, Reglamento
from .forms import SuscribirseForm
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from io import StringIO
import os, time

class SinPrivilegios(PermissionRequiredMixin):
    login_url='generales:sin_privilegios'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class HomePage(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Pagina de Inicio')

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/home.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        sedes = Sedes.objects.all().order_by('ciudad', 'nombre_sede')
        noticias = Noticias.objects.filter(modificado__lt=date.today())[:25]
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                noticias=noticias,
                sedes=sedes
            )
        )

class MiempresaView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/miempresa.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        emp = Miempresa.objects.all().last()
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                emp=emp
            )
        )

class PrincipiosView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/principios.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        emp = Miempresa.objects.all().last()
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                emp=emp
            )
        )        

class HimnoView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/himno.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        emp = Miempresa.objects.all().last()
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                emp=emp
            )
        ) 

class BienestarView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/bienestar.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        bienestar = Bienestar.objects.all().order_by('modificado')
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                bienestar=bienestar
            )
        ) 

class OcupacionalView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/ocupacional.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        ocupacional = Ocupacional.objects.all().order_by('-modificado')
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                ocupacional=ocupacional
            )
        ) 

class ReglamentoView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/reglamento.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        reglamento = Reglamento.objects.get(sede=self.request.user.profile.sede)
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                reglamento=reglamento
            )
        ) 

class OrganigramaView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/org.html'
    login_url='generales:login'
    def get(self, request, *args, **kwargs):
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year
            )
        ) 

class SedesView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/sedes.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        sedes = Sedes.objects.all().order_by('ciudad', 'nombre_sede')
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                sedes=sedes,
                hoy=date.today(),
                anor=date.today().year
            )
        )


class ContactoView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/contacto.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                hoy=date.today(),
                anor=date.today().year
            )
        )


def get_ajaxEnviar(request, *args, **kwargs): 
    msg = request.GET.get('msg', None)
    print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", msg)
    if not msg:
        return JsonResponse(data={'result': '', 'errors': 'No ha escrito mensage alguno.'})
    else:
        out = StringIO()
        subject = "CONTACTO GENTE INRAI "+request.user.first_name+' '+request.user.last_name
        message = msg
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['hebel.borrero@sistemainrai.net','recursoshumanos@sistemainrai.net']
        msg = EmailMessage(subject, message, email_from, recipient_list)
        result = msg.send(fail_silently=False)

        if result == 1:
            return JsonResponse(
            {
                'content': {
                    'message': 'Su mensaje ha sido enviado correctamente','errors': '',
                }
            }
        )
        else: 
            return JsonResponse(
            {
                'content': {
                    'message': 'Su mensaje no puedo ser enviado','errors': 'error al enviar',
                }
            }
        )

class DetalleSedeView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/detalle_sede.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        sede = Sedes.objects.get(id=kwargs["pk"])
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                sede=sede,
                hoy=date.today(),
                anor=date.today().year
            )
        )

class NoticiasView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/noticias.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        sedes = Sedes.objects.all().order_by('ciudad', 'nombre_sede')
        
        recientes = Noticias.objects.filter(modificado__gte=date.today())[:25]
        #self.object = None
        try:
            noticias = Noticias.objects.filter(modificado__lt=date.today())[:25]
            paginator1 = Paginator(noticias, 6)
        except:
            noticias = Noticias.objects.filter(modificado__lt=date.today())[:25]
            paginator1 = Paginator(noticias, 6)
        try:
            page2 = int(request.GET.get('page', '1'))
        except ValueError:
            page2 = 1
        try:
            noticias = paginator1.page(page2)
        except (EmptyPage, InvalidPage):
            noticias = paginator1.page(paginator1.num_pages)

        return self.render_to_response(
            self.get_context_data(
                hoy=date.today(),
                sedes=sedes,
                noticias=noticias,
                recientes=recientes,
                paginator1=paginator1,
                anor=date.today().year
            )
        )

def get_ajaxBuscar(request, *args, **kwargs): 
    buscar = request.GET.get('buscar', None)
    if not buscar:
        return JsonResponse(data={'result': '', 'errors': 'No encuentro noticias con "'+buscar+'"'})
    else:
        noticias = Noticias.objects.filter(titulo__icontains=buscar, subtitulo__icontains=buscar).order_by('-id')
        if noticias:
            return JsonResponse(data=noticias, safe=False)
        else: 
            return JsonResponse(data={'result': '', 'errors': 'No encuentro noticias con "'+buscar+'"'})
            
def HomeView(request):
    template_name = 'generales/home.html'
    hoy = date.today()
    total_mes = Noticias.objects.filter(modificado__date__month=hoy.month).count()
    titulares1 = Noticias.objects.filter(orden_destacado=0).order_by('-id')[:2]
    titulares2 = Noticias.objects.filter(orden_destacado=0).order_by('-id')[:4]
    titulares3 = Noticias.objects.filter(orden_destacado=0).order_by('-id')[:4]
    ultima_hora = Noticias.objects.filter(ultima_hora=True).order_by('-id')[:4]
    deportes1 = Noticias.objects.filter(orden_destacado=1, ultima_hora=False).last()
    deportes2 = Noticias.objects.filter(orden_destacado=2, ultima_hora=False).last()
    deportes3 = Noticias.objects.filter(orden_destacado__gte=3, ultima_hora=False).last()
    deportes4 = Noticias.objects.filter(orden_destacado=4, ultima_hora=False).last()
    loquepasa = Noticias.objects.filter(ultima_hora=False).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    loquesuena = Noticias.objects.filter(ultima_hora=False).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    loquesemueve = Noticias.objects.filter(ultima_hora=False).exclude(fecha_inicio_publicacion__gte=hoy).order_by('-id')[:8]
    sonajero = Noticias.objects.filter(ultima_hora=False).order_by('-id')[:8]
    recientes = Noticias.objects.filter(ultima_hora=False).order_by('-id')[:3]
    tecno1 = Noticias.objects.filter(ultima_hora=False, orden_destacado=0).order_by('-id')[:2]
    tecno2 = Noticias.objects.filter(ultima_hora=False).order_by('-id')[:4]
    lomasvisto = Noticias.objects.filter(ultima_hora=False).order_by('-vistas')[:4]
    populares = Noticias.objects.filter(ultima_hora=False).order_by('-vistas')[:4]
    if not deportes3:
        deportes3 = Noticias.objects.filter(orden_destacado__gte=3, ultima_hora=False).last()
    if not ultima_hora:
        ultima_hora = Noticias.objects.all().order_by('-id')[:3]

    context = {'hoy': hoy,
        'tecno1': tecno1,
        'tecno2': tecno2,
        'lomasvisto': lomasvisto,
        'populares': populares,
        'recientes': recientes,
        'titulares1': titulares1,
        'sonajero': sonajero,
        'loquesuena': loquesuena,
        'loquesemueve': loquesemueve,
        'titulares2': titulares2,
        'titulares3': titulares3,
        'loquepasa': loquepasa,
        'ultima_hora': ultima_hora,
        'deportes1': deportes1,
        'deportes2': deportes2,
        'deportes3': deportes3,
        'deportes4': deportes4,
        'anor': hoy.year
        }
    manana = hoy + timedelta(days=1)
    

    if request.POST.get('email'):
        form_home = SuscribirseForm(request.POST)
        if form_home.is_valid():
            post = form_home.save(commit=False)
            post.save()
            success_url=reverse_lazy("/")
            
            return JsonResponse(
                {
                    'content': {
                        'message': 'Gracias por suscribirse.',
                    }
                }
            )
        else:
            return JsonResponse(
                {
                    'content': {
                        'message': 'Ya ha sido registrado. Gracias!',
                    }
                }
            )
    else:
        form_home = SuscribirseForm()
        
    if request.POST.get('buscar'):
        buscar = (request.POST.get('buscar').upper())
        template_name="generales/search.html"
        try:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        except:
            resultado = Noticias.objects.filter(titulo__icontains=buscar).order_by('-id')
            #paginator5 = Paginator(resultado, 10)
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        #try:
        #    resultado = paginator5.page(page)
        #except (EmptyPage, InvalidPage):
        #    resultado = paginator5.page(paginator5.num_pages)

        #context['paginator5'] = paginator5
        context['form_search'] = resultado
    else:
        buscar = ''
        resultado={}
        template_name = "generales/home.html"

    
    sede1=Sedes.objects.all().order_by('nombre_sede')
    sedes=[]
    for i, item in enumerate(sede1):
        val = Noticias.objects.filter(modificado__date__month=hoy.month, autor__profile__sede=item.id).count()
        sedes.append({'nombre':item.nombre_sede, 'valor':int(round(val * 100 / 220, 0))}) # 200 notas / mes como meta minima de produccion de contenido.

    #sedes=Sedes.objects.filter(id__gt=sede1.id).order_by('nombre_sede')
    context['form_home'] = form_home
    context['resultado'] = resultado
    context['total_mes'] = total_mes
    context['total_porc_mes'] = int(round(total_mes * 100 /1540, 0))  # 1540 noticias en total por mes
    context["tit"] = nombre_mes(hoy.month)+" DE "+str(hoy.year)
    context['sedes'] = sedes
    #context['sede1'] = sede1

    return render(request, template_name, context)


class HomeSinPrivilegios(generic.TemplateView):
    template_name="generales/msg_sin_privilegios.html"


def nombre_mes(mesr):
    mesr=int(mesr)
    if mesr == 1:
        cmesr="ENERO"
    elif mesr == 2:
        cmesr="FEBRERO"
    elif mesr == 3:
        cmesr="MARZO"
    elif mesr == 4:
        cmesr="ABRIL"
    elif mesr == 5:
        cmesr="MAYO"
    elif mesr == 6:
        cmesr="JUNIO"
    elif mesr == 7:
        cmesr="JULIO"
    elif mesr == 8:
        cmesr="AGOSTO"
    elif mesr == 9:
        cmesr="SEPTIEMBRE"
    elif mesr == 10:
        cmesr="OCTUBRE"
    elif mesr == 11:
        cmesr="NOVIEMBRE"
    elif mesr == 12:
        cmesr="DICIEMBRE"

    return(cmesr)


def PoliticaView(request):
    hoy = date.today()
    anor = hoy.year
    
    return render(request, 'generales/privacy-policy.html')

