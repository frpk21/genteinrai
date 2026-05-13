import csv
import os
import time
from collections import namedtuple
from datetime import date, datetime, timedelta
from io import StringIO

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connections
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from generales.forms import MesAnoForm
from .forms import SuscribirseForm, ComentarioForm
from .models import (
    Bienestar, Elmuro, Funcionarios, Home1, io_funcionarios, Miempresa,
    Noticias, Ocupacional, Reglamento, Sedes, Tipos_tutoriales, Tutoriales,
)


GRUPOS_CTRL_HORARIOS = ('administradores', 'subadmin')


class CtrlHorariosAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo usuarios autenticados que pertenezcan a administradores o subadmin."""
    login_url = 'generales:login'
    raise_exception = False

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (
            u.is_superuser or u.groups.filter(name__in=GRUPOS_CTRL_HORARIOS).exists()
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.login_url))
        return HttpResponseRedirect(reverse_lazy('generales:sin_privilegios'))

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
        #sedes = Sedes.objects.all().order_by('ciudad', 'nombre_sede')
        #noticias = Noticias.objects.filter(modificado__lt=date.today())[:25]
        #elmuro = Elmuro.objects.all().order_by('-modificado')[:7]
        home1 = Home1.objects.all().last()
        self.object = None

        return self.render_to_response(
            self.get_context_data(
                anor=date.today().year,
                home1=home1
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

def _parse_fecha(value, default=None):
    if not value:
        return default
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return default


def _construir_reporte(funcionarios, fecha_inicio, fecha_fin):
    """Genera filas de reporte: una por (funcionario, fecha) en el rango."""
    dias = (fecha_fin - fecha_inicio).days + 1
    for funcionario in funcionarios:
        for i in range(dias):
            fecha = fecha_inicio + timedelta(days=i)
            yield {
                'funcionario': funcionario,
                'fecha': fecha,
                'resumen': io_funcionarios.resumen_jornada(funcionario, fecha),
                'estado': io_funcionarios.calcular_estado_asistencia(funcionario, fecha),
            }


class ctrl_horariosView(CtrlHorariosAccessMixin, generic.TemplateView):
    template_name = 'generales/ctrl_horarios_sedes.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        hoy = date.today()
        fecha = _parse_fecha(request.GET.get('fecha'), hoy)

        sede_id = request.GET.get('sede')
        sede = None
        if sede_id:
            try:
                sede = Sedes.objects.get(id=int(sede_id))
            except (Sedes.DoesNotExist, ValueError, TypeError):
                sede = None
        if sede is None:
            sede = getattr(getattr(request.user, 'profile', None), 'sede', None)
            if sede is None:
                sede = Sedes.objects.order_by('nombre_sede').first()

        return self.render_to_response(
            self.get_context_data(
                anor=hoy.year,
                fecha=fecha,
                sedes=Sedes.objects.filter(id=sede.id) if sede else Sedes.objects.none(),
                sedes2=Sedes.objects.all().order_by('nombre_sede'),
                filtro_sede=sede.id if sede else None,
                filtro_fecha=fecha,
            )
        )


class ctrl_horariosDetalleView(CtrlHorariosAccessMixin, View):
    """Detalle de asistencia: por sede o por un funcionario específico, en un rango opcional."""

    def get(self, request):
        hoy = date.today()
        pk = request.GET.get('pk')
        funcionario_id = request.GET.get('funcionario_id')
        fecha = _parse_fecha(request.GET.get('fecha'), hoy)
        fecha_inicio = _parse_fecha(request.GET.get('fecha_inicio'), fecha)
        fecha_fin = _parse_fecha(request.GET.get('fecha_fin'), fecha)

        if fecha_fin < fecha_inicio:
            fecha_inicio, fecha_fin = fecha_fin, fecha_inicio
        if (fecha_fin - fecha_inicio).days > 90:
            return JsonResponse({'error': 'El rango no puede superar 90 días'}, status=400)

        if funcionario_id:
            try:
                funcionarios = Funcionarios.objects.filter(id=int(funcionario_id))
            except (ValueError, TypeError):
                return JsonResponse({'error': 'funcionario_id inválido'}, status=400)
            if not funcionarios.exists():
                return JsonResponse({'error': 'Funcionario no encontrado'}, status=404)
        else:
            try:
                sede_pk = int(pk) if pk else 0
            except (ValueError, TypeError):
                return JsonResponse({'error': 'pk inválido'}, status=400)
            funcionarios = Funcionarios.objects.filter(sede=sede_pk).order_by('nombre1', 'apellido1')

        reporte = list(_construir_reporte(funcionarios, fecha_inicio, fecha_fin))

        return JsonResponse({
            'content': {
                'tbl_rs': render_to_string('generales/trafico.html', {'reporte': reporte})
            }
        })


class BuscarFuncionarioView(CtrlHorariosAccessMixin, View):
    """Autocomplete: busca funcionarios por cédula o nombre. Devuelve JSON."""

    def get(self, request):
        q = (request.GET.get('q') or '').strip()
        if len(q) < 2:
            return JsonResponse({'results': []})
        qs = Funcionarios.objects.filter(
            Q(cedula__icontains=q) |
            Q(nombre1__icontains=q) |
            Q(nombre2__icontains=q) |
            Q(apellido1__icontains=q) |
            Q(apellido2__icontains=q)
        ).order_by('apellido1', 'nombre1')[:15]
        results = [{
            'id': f.id,
            'cedula': f.cedula,
            'nombre': f"{f.nombre1} {f.nombre2 or ''} {f.apellido1} {f.apellido2 or ''}".strip(),
            'sede': f.sede.nombre_sede if f.sede_id else '',
            'cargo': f.cargo.nombre if f.cargo_id else '',
        } for f in qs]
        return JsonResponse({'results': results})


class ExportarAsistenciaCSVView(CtrlHorariosAccessMixin, View):
    """Exporta el rango como CSV (UTF-8 con BOM para Excel en Windows)."""

    def get(self, request, *args, **kwargs):
        sede_id = request.GET.get('sede')
        funcionario_id = request.GET.get('funcionario_id')
        fecha_inicio = _parse_fecha(request.GET.get('fecha_inicio'))
        fecha_fin = _parse_fecha(request.GET.get('fecha_fin'))

        if not fecha_inicio or not fecha_fin:
            return HttpResponse('Fechas inválidas', status=400)
        if fecha_fin < fecha_inicio:
            fecha_inicio, fecha_fin = fecha_fin, fecha_inicio
        if (fecha_fin - fecha_inicio).days > 366:
            return HttpResponse('El rango no puede superar 1 año', status=400)

        nombre_archivo = 'asistencia'
        if funcionario_id:
            try:
                funcionarios = Funcionarios.objects.filter(id=int(funcionario_id))
            except (ValueError, TypeError):
                return HttpResponse('funcionario_id inválido', status=400)
            if not funcionarios.exists():
                return HttpResponse('Funcionario no encontrado', status=404)
            f = funcionarios.first()
            nombre_archivo = f'asistencia_{f.cedula}'
        elif sede_id:
            try:
                sede = Sedes.objects.get(id=int(sede_id))
            except (Sedes.DoesNotExist, ValueError, TypeError):
                return HttpResponse('Sede inválida', status=400)
            funcionarios = Funcionarios.objects.filter(sede=sede).order_by('nombre1', 'apellido1')
            nombre_archivo = f'asistencia_{sede.nombre_sede}'
        else:
            return HttpResponse('Debe indicar sede o funcionario_id', status=400)

        header = [
            'Cedula', 'Funcionario', 'Sede', 'Fecha', 'Entrada esperada', 'Salida esperada',
            'Entrada', 'Inicio almuerzo', 'Fin almuerzo', 'Salida',
            'Retardo', 'Salida anticipada', 'Ausente', 'Horas trabajadas',
        ]

        class _Echo:
            def write(self, value):
                return value

        writer = csv.writer(_Echo(), quoting=csv.QUOTE_MINIMAL)

        def filas():
            yield '﻿'  # BOM UTF-8 para Excel
            yield writer.writerow(header)
            for fila in _construir_reporte(funcionarios, fecha_inicio, fecha_fin):
                fn = fila['funcionario']
                r = fila['resumen']
                e = fila['estado']
                yield writer.writerow([
                    fn.cedula,
                    f"{fn.nombre1} {fn.nombre2 or ''} {fn.apellido1} {fn.apellido2 or ''}".strip(),
                    fn.sede.nombre_sede if fn.sede_id else '',
                    fila['fecha'].strftime('%Y-%m-%d'),
                    fn.hora_entrada.strftime('%H:%M') if fn.hora_entrada else '',
                    fn.hora_salida.strftime('%H:%M') if fn.hora_salida else '',
                    r['entrada'].strftime('%H:%M:%S') if r['entrada'] else '',
                    r['inicio_almuerzo'].strftime('%H:%M:%S') if r['inicio_almuerzo'] else '',
                    r['fin_almuerzo'].strftime('%H:%M:%S') if r['fin_almuerzo'] else '',
                    r['salida'].strftime('%H:%M:%S') if r['salida'] else '',
                    'Si' if e['retardo'] else 'No',
                    'Si' if e['salida_anticipada'] else 'No',
                    'Si' if e['ausente'] else 'No',
                    f"{e['horas_trabajadas']:.2f}" if e['horas_trabajadas'] is not None else '',
                ])

        response = StreamingHttpResponse(filas(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = (
            f'attachment; filename="{nombre_archivo}_{fecha_inicio}_{fecha_fin}.csv"'
        )
        return response


class KioskoView(CtrlHorariosAccessMixin, generic.TemplateView):
    """Pantalla fullscreen para fichar entrada/salida con lector de código de barras USB."""
    template_name = 'generales/kiosko.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['anor'] = date.today().year
        return ctx


class KioskoRegistrarView(CtrlHorariosAccessMixin, View):
    """Recibe la cédula leída por el escáner USB y crea el evento que corresponda.

    Lógica de tipo de evento (state machine simple por día):
    - sin eventos -> ENTRADA
    - solo ENTRADA -> INICIO_ALMUERZO
    - ENTRADA + INICIO_ALMUERZO -> FIN_ALMUERZO
    - ENTRADA + INICIO + FIN -> SALIDA
    - ya hay SALIDA -> nueva ENTRADA (segundo turno) -- pero responde "ya cerró jornada"

    Debounce: si la última lectura de la misma cédula fue hace < 5s, rechaza.
    """

    DEBOUNCE_SEGUNDOS = 5

    def post(self, request):
        cedula = (request.POST.get('cedula') or '').strip()
        if not cedula:
            return JsonResponse({'ok': False, 'error': 'Cédula vacía'}, status=400)

        # Permitir códigos con prefijos o caracteres no numéricos -- nos quedamos con los dígitos.
        cedula_limpia = ''.join(ch for ch in cedula if ch.isdigit())
        if not cedula_limpia:
            return JsonResponse({'ok': False, 'error': 'Código inválido', 'codigo': cedula}, status=400)

        try:
            funcionario = Funcionarios.objects.select_related('sede').get(cedula=cedula_limpia)
        except Funcionarios.DoesNotExist:
            return JsonResponse({
                'ok': False,
                'error': 'Cédula no registrada',
                'codigo': cedula_limpia,
            }, status=404)

        ahora = datetime.now()
        hoy = ahora.date()
        eventos_hoy = list(io_funcionarios.eventos_del_dia(funcionario, hoy))

        if eventos_hoy:
            ultimo = eventos_hoy[-1]
            dt_ultimo = datetime.combine(hoy, ultimo.hora)
            if (ahora - dt_ultimo).total_seconds() < self.DEBOUNCE_SEGUNDOS:
                return JsonResponse({
                    'ok': False,
                    'error': 'Lectura duplicada, espere unos segundos',
                    'funcionario': str(funcionario),
                }, status=429)

        tipos_registrados = {e.tipo_evento for e in eventos_hoy}
        if io_funcionarios.EVENTO_ENTRADA not in tipos_registrados:
            tipo = io_funcionarios.EVENTO_ENTRADA
        elif io_funcionarios.EVENTO_INICIO_ALMUERZO not in tipos_registrados:
            tipo = io_funcionarios.EVENTO_INICIO_ALMUERZO
        elif io_funcionarios.EVENTO_FIN_ALMUERZO not in tipos_registrados:
            tipo = io_funcionarios.EVENTO_FIN_ALMUERZO
        elif io_funcionarios.EVENTO_SALIDA not in tipos_registrados:
            tipo = io_funcionarios.EVENTO_SALIDA
        else:
            tipo = io_funcionarios.EVENTO_OTRO

        evento = io_funcionarios.objects.create(
            funcionario=funcionario,
            fecha=hoy,
            hora=ahora.time(),
            tipo_evento=tipo,
        )

        foto_url = ''
        try:
            if funcionario.foto and hasattr(funcionario.foto, 'url'):
                foto_url = funcionario.foto.url
        except Exception:
            foto_url = ''

        return JsonResponse({
            'ok': True,
            'funcionario': {
                'id': funcionario.id,
                'nombre': f"{funcionario.nombre1} {funcionario.nombre2 or ''} {funcionario.apellido1} {funcionario.apellido2 or ''}".strip(),
                'cedula': funcionario.cedula,
                'sede': funcionario.sede.nombre_sede if funcionario.sede_id else '',
                'foto': foto_url,
            },
            'evento': {
                'tipo': tipo,
                'tipo_display': evento.get_tipo_evento_display(),
                'fecha': hoy.strftime('%Y-%m-%d'),
                'hora': ahora.strftime('%H:%M:%S'),
            },
        })

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

class ElmuroView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/elmuro.html'
    login_url='generales:login'
    success_url=reverse_lazy("generales:elmuro")

    def get(self, request, *args, **kwargs):
        self.object = None
        tipos = Tipos_tutoriales.objects.all().order_by('nombre')
        try:
            elmuro = Elmuro.objects.all().order_by('-modificado')[:25]
            paginator1 = Paginator(elmuro, 4)
        except:
            elmuro = Elmuro.objects.all().order_by('-modificado')[:25]
            paginator1 = Paginator(elmuro, 4)
        try:
            page2 = int(request.GET.get('page', '1'))
        except ValueError:
            page2 = 1
        try:
            elmuro = paginator1.page(page2)
        except (EmptyPage, InvalidPage):
            elmuro = paginator1.page(paginator1.num_pages)

        return self.render_to_response(
            self.get_context_data(
                hoy=date.today(),
                tipos=tipos,
                elmuro=elmuro,
                paginator1=paginator1,
                form_com = ComentarioForm(),
                anor=date.today().year
            )
        )


    def post(self, request, *args, **kwargs):
        form_com = ComentarioForm(request.POST, request.FILES)
        if form_com.is_valid():
            post = form_com.save(commit=False)
            post.autor = self.request.user
            post.save()
            form_com = ComentarioForm()
            return HttpResponseRedirect(self.success_url)

class TutorialesView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/tutoriales.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        tipos = Tipos_tutoriales.objects.all().order_by('nombre')
        try:
            tutoriales = Tutoriales.objects.all()[:24]
            paginator1 = Paginator(tutoriales, 4)
        except:
            tutoriales = Tutoriales.objects.all()[:24]
            paginator1 = Paginator(tutoriales, 4)
        try:
            page2 = int(request.GET.get('page', '1'))
        except ValueError:
            page2 = 1
        try:
            tutoriales = paginator1.page(page2)
        except (EmptyPage, InvalidPage):
            tutoriales = paginator1.page(paginator1.num_pages)

        return self.render_to_response(
            self.get_context_data(
                hoy=date.today(),
                tipos=tipos,
                tutoriales=tutoriales,
                paginator1=paginator1,
                anor=date.today().year
            )
        )



def ajax_update(request, *args, **kwargs):
    buscar = request.GET.get('buscar', None)
    tutoriales = Tutoriales.objects.filter(titulo__icontains=buscar.upper()).order_by('-id')
    if tutoriales:
        return JsonResponse(data={'buscar': buscar, 'errors': ''})
    else:
        return JsonResponse(data={'buscar': '', 'errors': 'No encontre tutoriales..'})
    #return render(request, "generales/tutoriales.html", {'tutoriales': tutoriales, 'paginator1': paginator1, 'hoy':date.today(), 'tipos':Tipos_tutoriales.objects.all().order_by('nombre'), 'anor': date.today().year})



class UpdtutorialesView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/tutoriales.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        buscar = kwargs["pk"]
        try:
            tutoriales = Tutoriales.objects.filter(titulo__icontains=buscar.upper()).order_by('-id')
            paginator1 = Paginator(tutoriales, 6)
        except:
            tutoriales = Tutoriales.objects.filter(titulo__icontains=buscar.upper()).order_by('-id')
            paginator1 = Paginator(tutoriales, 6)
        try:
            page2 = int(request.GET.get('page', '1'))
        except ValueError:
            page2 = 1
        try:
            tutoriales = paginator1.page(page2)
        except (EmptyPage, InvalidPage):
            tutoriales = paginator1.page(paginator1.num_pages)

        return self.render_to_response(
            self.get_context_data(
                hoy=date.today(),
                tipos=Tipos_tutoriales.objects.all().order_by('nombre'),
                tutoriales=tutoriales,
                paginator1=paginator1,
                anor=date.today().year
            )
        )



class TipoTutorialView(LoginRequiredMixin, generic.TemplateView):
    template_name='generales/tutoriales.html'
    login_url='generales:login'

    def get(self, request, *args, **kwargs):
        tipos = Tipos_tutoriales.objects.all().order_by('nombre')
        try:
            tutoriales = Tutoriales.objects.filter(tipo=kwargs["pk"])[:25]
            paginator1 = Paginator(tutoriales, 6)
        except:
            tutoriales = Tutoriales.objects.filter(tipo=kwargs["pk"])[:25]
            paginator1 = Paginator(tutoriales, 6)
        try:
            page2 = int(request.GET.get('page', '1'))
        except ValueError:
            page2 = 1
        try:
            tutoriales = paginator1.page(page2)
        except (EmptyPage, InvalidPage):
            tutoriales = paginator1.page(paginator1.num_pages)

        return self.render_to_response(
            self.get_context_data(
                hoy=date.today(),
                tipos=tipos,
                tutoriales=tutoriales,
                paginator1=paginator1,
                anor=date.today().year
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

