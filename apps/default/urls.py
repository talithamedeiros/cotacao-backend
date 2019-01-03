# -*- coding: utf-8 -*-

##################################################
#				DJANGO IMPORTS                   #
##################################################
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
##################################################

##################################################
#				CUSTOM IMPORTS                   #
##################################################
from . import views
##################################################


urlpatterns = (
    # url(r'^auth/login/$', Login.as_view(), name="login"),
    url(r'^auth/register/$', views.Register.as_view(), name="register"),
    url(r'^auth/logout/$', login_required(views.Logout.as_view()), name="logout"),
    url(r'^dashboard/$', login_required(views.Dashboard.as_view()), name="home"),
    url(r'^service/cnpj/', login_required(views.get_cnpj_json), name="service-cnpj"),
    url(r'^service/cep/', login_required(views.get_cep_json), name="service-cep"),
)
