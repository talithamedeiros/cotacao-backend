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
from .models import *
from .forms import *
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

        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))

        return render (request, 'account/register.html', {'form':form})

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
                user.is_admin =  True
                user.save()
                return redirect(reverse_lazy("dashboard"))

            else:
                form = RegisterForm()

        return render(request, 'account/register.html', {'form': form})


class Login(JSONResponseMixin,View):
    def get(self, request):
        form = LoginForm
        
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))

        return render (request, 'account/login.html', {'form':form})

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
                    return redirect(reverse_lazy("dashboard"))
                else:
                    context['error'] = "Usuario não ativo"
                    return render(request, 'account/login.html',{'form':form,'context':context})
            else:
                context['error'] = "Usuário não cadastrado"
                return render(request, 'account/login.html',{'form':form,'context':context})
        else:
            form = LoginForm()

        return render(request, 'account/login.html', {'form': form})


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
    template_name = "dashboard/dashboard.html"

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


'''
----------------------------------------
            PARAMETRO
----------------------------------------
'''
class ParametroList(ListView):
    template_name = "parametro/list.html"

    def get(self, request):

        parametro = SeguradoraParametro.objects.all()
        context = {'parametro': parametro}
        return render(request, self.template_name, context)


class ParametroCreate(View):
    template_name = "parametro/create.html"

    def get(self, request):
        form = SeguradoraParametroForm()

        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SeguradoraParametroForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect(reverse("parametro-list"))

        context = {'form':form}
        return render(request, self.template_name, context)


class ParametroUpdate(View):
    template_name = "parametro/update.html"

    def get(self, request, pk):
        parametro = SeguradoraParametro.objects.get(pk=pk)
        form = SeguradoraParametroForm(instance=parametro)

        context = {'form':form, 'parametro':parametro}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        parametro = SeguradoraParametro.objects.get(pk=pk)
        form = SeguradoraParametroForm(request.POST, request.FILES, instance=parametro)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect(reverse("parametro-list"))

        context = {'form':form, 'parametro':parametro}
        return render(request, self.template_name, context)


class ParametroDelete(View):
    def get(self, request, pk):
        parametro = SeguradoraParametro.objects.get(pk=pk).delete()
        return redirect(reverse("parametro-list"))


'''
----------------------------------------
            SEGURADORA
----------------------------------------
'''
class SeguradoraList(ListView):
    template_name = "seguradora/list.html"

    def get(self, request):

        seguradora = Seguradora.objects.all()
        context = {'seguradora': seguradora}
        return render(request, self.template_name, context)


class SeguradoraCreate(View):
    template_name = "seguradora/create.html"

    def get(self, request):
        form = SeguradoraForm()

        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = SeguradoraForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect(reverse("seguradora-list"))

        context = {'form':form}
        return render(request, self.template_name, context)


class SeguradoraUpdate(View):
    template_name = "seguradora/update.html"

    def get(self, request, pk):
        seguradora = Seguradora.objects.get(pk=pk)
        form = SeguradoraForm(instance=seguradora)

        context = {'form':form, 'seguradora':seguradora}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        seguradora = Seguradora.objects.get(pk=pk)
        form = SeguradoraForm(request.POST, request.FILES, instance=seguradora)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            return redirect(reverse("seguradora-list"))

        context = {'form':form, 'seguradora':seguradora}
        return render(request, self.template_name, context)


class SeguradoraDelete(View):
    def get(self, request, pk):
        seguradora = Seguradora.objects.get(pk=pk).delete()
        return redirect(reverse("seguradora-list"))