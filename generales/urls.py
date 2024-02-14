from django.urls import include, path
from generales import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^$', HomeView, name='home'),
    #path('',HomeView, name='home'),
    path('',views.Home.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='generales/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='generales/login.html'), name='logout'),
    path('loginunlock/', auth_views.LoginView.as_view(template_name='generales/lock.html'), name='loginunlock'),
    path('sin_privilegios/', views.HomeSinPrivilegios.as_view(), name='sin_privilegios'),
    path('sedes/', views.SedesView.as_view(), name='sedes'),
    path('sedes/detalle/<int:pk>', views.DetalleSedeView.as_view(), name='detalle_sede'),
    path('noticias/', views.NoticiasView.as_view(), name='noticias'),
    url((r'^politica/$'), views.PoliticaView, name="politica"),
    path('busca/', views.get_ajaxBuscar, name='find_post'),
    path('comp/', views.MiempresaView.as_view(), name='miempresa'),
    path('comp/principios', views.PrincipiosView.as_view(), name='principios'),
    path('comp/himno', views.HimnoView.as_view(), name='himno'),
    path('comp/bienestar', views.BienestarView.as_view(), name='bienestar'),
    path('comp/ocupacional', views.OcupacionalView.as_view(), name='ocupacional'),
    path('elmuro', views.ElmuroView.as_view(), name='elmuro'),
    path('tutoriales', views.TutorialesView.as_view(), name='tutoriales'),
    path('comp/reglamento', views.ReglamentoView.as_view(), name='reglamento'),
    path('comp/org', views.OrganigramaView.as_view(), name='org'),
    path('contacto', views.ContactoView.as_view(), name='contacto'),
    path('enviar/', views.get_ajaxEnviar, name='enviar'),
    path('tutoriales/tp/<int:pk>', views.TipoTutorialView.as_view(), name='tipo_tutorial'),
    path('update/', views.ajax_update, name='upd'),
    path('update/tutoriales/<str:pk>', views.UpdtutorialesView.as_view(), name='updtuto'),
    path('ctrl_horarios/', views.ctrl_horariosView.as_view(), name='ctrl_horarios'),
    path('ctrl_horarios/trafic/', views.ctrl_horariosDetalleView.as_view(), name='ctrl_horarios_detalle'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 