#-*- coding: utf-8 -*-


##################################################
#               DJANGO IMPORTS                   #
##################################################
from django import forms
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField
##################################################


##################################################
#               CUSTOM IMPORTS                   #
##################################################
from .models import * # MODELS
##################################################


'''
---------------------------------------
            ADMIN AREA
---------------------------------------
'''

class UserCreationForm(forms.ModelForm):
    # Formulario para criacao de novos usuarios.Inclui todos os campos requeridos.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email',)

    def clean_password2(self):
        # Verifique se as duas entradas de senha correspondem
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Verifique se a senha fornecida esta no formato hash
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Um formulario para atualizar os usuarios . Inclui todos os campos
    de um usuario, mas substitui o campo de senha com administracao de
    hash de senha.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Retorna o valor inicial caso nao tenha acesso
        return self.initial["password"]

'''
---------------------------------------
            END ADMIN AREA
---------------------------------------
'''



'''
---------------------------------------
            AUTH FORMS
---------------------------------------
'''

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email:', max_length=75)
    password = forms.CharField(label='Senha:', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Email Fields widget
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu email'

        # Password Fields widget
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'
        pass


class RegisterForm(forms.Form):
    nome = forms.CharField(label='Nome:', max_length=45)
    sobrenome = forms.CharField(label='Sobrenome:', max_length=45)
    email = forms.EmailField(label='Email:', max_length=75)
    password = forms.CharField(label='Senha:', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Nome Fields widget
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['nome'].widget.attrs['placeholder'] = 'Digite seu nome'

        # Sobrenome Fields widget
        self.fields['sobrenome'].widget.attrs['class'] = 'form-control'
        self.fields['sobrenome'].widget.attrs['placeholder'] = 'Digite seu sobrenome'

        # Email Fields widget
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu email'

        # Password Fields widget
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'
        pass

'''
---------------------------------------
            END AUTH FORMS
---------------------------------------
'''


class SeguradoraParametroForm(forms.ModelForm):
    
    class Meta:
        model = SeguradoraParametro
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(SeguradoraParametroForm, self).__init__(*args, **kwargs)

        # GENERAL INFO
        self.fields['is_apartir'].widget.attrs['class'] = 'custom-control custom-checkbox custom-control-inline'
        self.fields['is_ate'].widget.attrs['class'] = 'custom-control custom-checkbox custom-control-inline'

        self.fields['a_partir'].widget.attrs['class'] = 'form-control'
        self.fields['ate'].widget.attrs['class'] = 'form-control'

        self.fields['seguradora'].widget.attrs['class'] = 'form-control'
        self.fields['taxa_seguro'].widget.attrs['class'] = 'form-control'


class SeguradoraForm(forms.ModelForm):
    
    class Meta:
        model = Seguradora
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(SeguradoraForm, self).__init__(*args, **kwargs)

        # GENERAL INFO
        self.fields['name'].widget.attrs['class'] = 'form-control'
