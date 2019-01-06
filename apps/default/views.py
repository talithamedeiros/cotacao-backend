#-*- coding: utf-8 -*-

##################################################
#				DJANGO IMPORTS                   #
##################################################
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import RedirectView, View, UpdateView, ListView, DetailView, DeleteView
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.forms import formset_factory
from django.db.models import Count, Avg
import pandas as pd
from pandas import DataFrame
import numpy as np
##################################################



##################################################
#				CUSTOM IMPORTS                   #
##################################################
from .models import Usuario
from .forms import LoginForm, RegisterForm # AUTH FORMS
import requests
import re
from datetime import datetime
##################################################


'''
    CONVERT TO JSON
'''

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


'''
----------------------------------------
            AUTH METHODS
----------------------------------------
'''

class Register(JSONResponseMixin,View):
    def get(self, request):
        form = RegisterForm
        return render (request, 'default/register.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            email = request.POST['email']
            password = request.POST['password']

            if not nome:
                context['error_msg'] = 'nome cannot be empty !'
            if not sobrenome:
                context['error_msg'] = 'sobrenome cannot be empty !'
            if not email:
                context['error_msg'] = 'email cannot be empty !'
            if not password:
                context['error_msg'] = 'password cannot be empty !'

            if not context:
                user = Usuario.objects.create_user(email, password)
                user.nome = nome
                user.sobrenome = sobrenome
                user.is_active =  True
                user.save()
                return redirect(reverse_lazy("home"))

            else:
                form = RegisterForm()

        return render(request, 'default/register.html', {'form': form})


class Login(JSONResponseMixin,View):
    def get(self, request):
        form = LoginForm
        return render (request, 'default/login.html', {'form':form})

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            form = LoginForm(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse_lazy("home"))
                else:
                    context['error'] = "Usuario não ativo"
                    return render(request, 'default/login.html',{'form':form,'context':context})
            else:
                context['error'] = "Usuário não cadastrado"
                return render(request, 'default/login.html',{'form':form,'context':context})
        else:
            form = LoginForm()

        return render(request, 'default/login.html', {'form': form})


class Logout(JSONResponseMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')


'''
----------------------------------------
            END AUTH METHODS
----------------------------------------
'''

'''
    DASHBOARD
'''

class Dashboard(View):
    template_name = "dashboard.html"

    def get(self, request):

        context = {}
        return render(request, self.template_name, context)


'''
----------------------------------------
            API'S INTEGRATION
----------------------------------------
'''

def get_cnpj_json(request):
    if request.method == 'GET':
        response = requests.get('http://receitaws.com.br/v1/cnpj/' + request.GET.get('cnpj')).json()
    return JsonResponse(response)


def get_cep_json(request):
    if request.method == 'GET':
        response = requests.get(
            'http://www.cepaberto.com/api/v2/ceps.json?cep=' + request.GET.get('cep'),
            headers={'Authorization': 'Token token=055cc8e8b0e25d6b6bb30a6dad8b1932'}
            ).json()
    return JsonResponse(response)
