#-*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Usuario, Seguradora, SeguradoraParametro, Pedido, Proposta
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # Formularios para adicionar ou alterar instancias dos usuarios
    form = UserChangeForm
    add_form = UserCreationForm

    # Os campos a serem no User model.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('nome', 'sobrenome', 'email', 'password', 'token')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    # Campos a serem exibidos no cadastro de um usuario no painel admin.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Registra as alteracoes no painel admin
admin.site.register(Seguradora)
admin.site.register(SeguradoraParametro)
admin.site.register(Pedido)
admin.site.register(Proposta)
admin.site.register(Usuario, UserAdmin)