from django.urls import include, path

from generales.views import HomeView, HomeSinPrivilegios, PoliticaView

from django.contrib.auth import views as auth_views
 
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^$', HomeView, name='home'),
    path('',HomeView, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='generales/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='generales/login.html'), name='logout'),
    path('loginunlock/', auth_views.LoginView.as_view(template_name='generales/lock.html'), name='loginunlock'),
    path('sin_privilegios/', HomeSinPrivilegios.as_view(), name='sin_privilegios'),
    url((r'^politica/$'), PoliticaView, name="politica"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 