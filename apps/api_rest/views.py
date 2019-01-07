from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status, generics, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_auth.registration.views import SocialLoginView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.db.models import Avg, Count, Q
from django.db import IntegrityError, transaction, connection

from oauth2_provider.models import Application, AccessToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.http import Http404
from django.conf import settings
from django.utils import formats
from django.template.loader import render_to_string
from oauthlib import common
from datetime import datetime, timedelta, date, timezone
import os, binascii
import requests
import hashlib
import json
import re

from decimal import Decimal

from apps.message_core.views import EmailThread, Sms
from apps.api_rest import serializers
from apps.default.models import Usuario, Pedido, Proposta, SeguradoraParametro


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class ConvertToken(generics.GenericAPIView):
    serializer_class = serializers.ConvertTokenSerializer

    def post(self,request):
        message = {}
        serializer = serializers.ConvertTokenSerializer(data=request.data)
        if serializer.is_valid():
            application = Application.objects.all()[0]
            token = Token.objects.get(key=serializer.data['key'])
            expires = datetime.now() + timedelta(seconds=100000000)
            access_token = AccessToken(
                user=token.user,
                scope='write read',
                expires=expires,
                token=common.generate_token(),
                application=application
            )
            access_token.save()
            message['token'] = access_token.token
            message['name'] = access_token.user.nome
            message['email'] = access_token.user.email
            return Response(message,200)
        else:
            message['status'] = 'error'
            return Response(message, 500)


class Login(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        context = {}
        user = ""
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            try:
                app = Application.objects.all()[0]
            except:
                context['msg'] = 'Application não encontrado'
                return Response(context, status=500)
            if user:
                login(request, user)
                client_auth = requests.auth.HTTPBasicAuth(app.client_id, app.client_secret)
                post_data = {"grant_type": "password", "username": email, "password": password}
                headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
                response = requests.post(settings.API_URL, auth=client_auth, data=post_data, headers=headers)

                try:
                    context = {
                        'name': user.nome,
                        'email': user.email,
                        'token': response.json()['access_token']
                    }
                except:
                    context = {
                        'name': user.nome,
                        'email': user.email,
                        'token': user.token
                    }
                return Response(context, status=200)
            else:
                context['status'] = 'incorrectPassword'
                context['msg'] = 'Senha incorreta.'
                return Response(context, status=409)

            return Response(context, status=200)
        else:
            return Response(serializer.errors, status=500)


class Register(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        context = {}
        serializer = serializers.RegisterSerializer(data=request.data)
        message = {}
        if serializer.is_valid():
            if Usuario.objects.filter(email=serializer.data['email']).exists():
                message = {'status': 'error', 'message': 'Email já cadastrado.'}
                return Response(message,status=500)
            else:
                try:
                    user = Usuario.objects.create_user(serializer.data['email'], serializer.data['password'])
                    user.nome = serializer.data['nome_completo']
                    user.nomecomleto = serializer.data['nome_completo']
                    user.is_active = True
                    user.token = binascii.b2a_hex(os.urandom(15))
                    user.save()
                except Exception as e:
                    user.delete()
                    message = {'status': 'error', 'message': str(e)}
                    return Response(message,status=500)
                
                try:
                    email_address = EmailAddress()
                    email_address.verified = False
                    email_address.user = user
                    email_address.email = user.email
                    email_address.save()

                except Exception as e:
                    user.delete()
                    email_address.delete()
                    message = {'status': 'error', 'message': str(e)}
                    return Response(message,status=500)
                    
            message = {'status':'success'}
            return Response(message,status=200)
        else:

            message = {'status':'error'}
            return Response(message,status=400)


class AppRegistration(generics.GenericAPIView):
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = serializers.AppRegistration
    def put(self, request, format=None):
        response = {}
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = Usuario.objects.get(pk=request.user.pk)
            user.registration_id = serializer.data['registration_id']
            user.save()
            return Response(response,status=200)
        return Response(response,status=500)


def get_valor_seguro(porcentagem, valor_bike):
    return (valor_bike * porcentagem) / 100


def save_proposta(seguradora, user, preco_seguro):
    json = {}
    proposta = Proposta()
    proposta.seguradora = seguradora
    proposta.usuario = user
    proposta.preco_seguro = preco_seguro
    proposta.save()

    json['seguradora'] = seguradora.name
    json['preco_seguro'] = str(Decimal(preco_seguro))

    return json


def save_array_propostas(query_consulta, user, valor_bike):
    retorno = None
    if query_consulta:
        retorno = []
        for child in query_consulta:
            retorno.append(save_proposta(child.seguradora, user, get_valor_seguro(child.taxa_seguro, Decimal(valor_bike))))
    return retorno


class CotarSeguro(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CotacaoSeguroSerializer

    def post(self, request, format=None):
        serializer = serializers.CotacaoSeguroSerializer(data=request.data)
        if serializer.is_valid():
            message = {}    
            valor_bike = serializer.data.get('valor_bike')

            pedido = Pedido()
            pedido.usuario = self.request.user
            pedido.valor_bike = valor_bike
            pedido.save()
            
            valor_seguro = 0
            is_atendido = False
            retorno_propostas = []
            retorno_funcao = None

            query_consulta = SeguradoraParametro.objects.filter(Q(a_partir__lte=valor_bike, ate__gte=valor_bike))

            retorno_funcao = save_array_propostas(query_consulta, self.request.user, valor_bike)

            if retorno_funcao != None:
                is_atendido = True
                retorno_propostas += retorno_funcao
            
            query_consulta = SeguradoraParametro.objects.filter(Q(a_partir__lte=valor_bike), Q(ate__isnull=True) | Q(ate=float(0)), Q(is_apartir=True))
            
            retorno_funcao = save_array_propostas(query_consulta, self.request.user, valor_bike)

            if retorno_funcao != None:
                is_atendido = True
                retorno_propostas += retorno_funcao

            query_consulta = SeguradoraParametro.objects.filter(Q(ate__gte=valor_bike), Q(a_partir__isnull=True) | Q(a_partir=float(0)), Q(is_ate=True))

            retorno_funcao = save_array_propostas(query_consulta, self.request.user, valor_bike)

            if retorno_funcao != None:
                is_atendido = True
                retorno_propostas += retorno_funcao

            retorno_propostas = json.dumps(retorno_propostas)

            if is_atendido == False:
                message['mensagem'] = 'Infelizmente não temos nenhuma proposta para você!'
                return Response(message, status=201)

            pedido = Pedido.objects.filter(pk=pedido.pk).update(is_atendido=is_atendido)

            return Response(retorno_propostas, status=201)
        return Response(serializer.errors, status=400)
