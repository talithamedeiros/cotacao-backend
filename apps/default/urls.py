# -*- coding: utf-8 -*-

##################################################
#				DJANGO IMPORTS                   #
##################################################
from django.urls import include, path, re_path
from django.contrib.auth.decorators import login_required
##################################################

##################################################
#				CUSTOM IMPORTS                   #
##################################################
from . import views
##################################################

urlpatterns = (
    # path('auth/login/', Login.as_view(), name="login"),
    path('auth/register/', views.Register.as_view(), name="register"),
    path('auth/logout/', login_required(views.Logout.as_view()), name="logout"),
    path('dashboard/', login_required(views.Dashboard.as_view()), name="dashboard"),
    path('service/cnpj/', login_required(views.get_cnpj_json), name="service-cnpj"),
    path('service/cep/', login_required(views.get_cep_json), name="service-cep"),
)
