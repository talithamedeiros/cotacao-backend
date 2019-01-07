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
    path('auth/login/', views.Login.as_view(), name="auth-login"),
    path('auth/register/', views.Register.as_view(), name="register"),
    path('auth/logout/', login_required(views.Logout.as_view()), name="logout"),
    path('dashboard/', login_required(views.Dashboard.as_view()), name="dashboard"),
    path('service/cnpj/', login_required(views.get_cnpj_json), name="service-cnpj"),
    path('service/cep/', login_required(views.get_cep_json), name="service-cep"),

    path('seguradora/parametro/list/', login_required(views.ParametroList.as_view()), name='parametro-list'),
    path('seguradora/parametro/create/', login_required(views.ParametroCreate.as_view()), name='parametro-create'),
    path('seguradora/parametro/update/<int:pk>/', login_required(views.ParametroUpdate.as_view()), name="parametro-update"),
    path('seguradora/parametro/delete/<int:pk>/', login_required(views.ParametroDelete.as_view()), name="parametro-delete"),

    path('seguradora/list/', login_required(views.SeguradoraList.as_view()), name='seguradora-list'),
    path('seguradora/create/', login_required(views.SeguradoraCreate.as_view()), name='seguradora-create'),
    path('seguradora/update/<int:pk>/', login_required(views.SeguradoraUpdate.as_view()), name="seguradora-update"),
    path('seguradora/delete/<int:pk>/', login_required(views.SeguradoraDelete.as_view()), name="seguradora-delete"),

)
