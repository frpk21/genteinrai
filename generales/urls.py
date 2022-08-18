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
    path('comp/org', views.OrganigramaView.as_view(), name='org'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 