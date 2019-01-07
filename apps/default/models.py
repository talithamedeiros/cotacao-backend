#-*- coding: utf-8 -*-
from django.db import models
from simple_history.models import HistoricalRecords
from django_extensions.db.models import TimeStampedModel
from model_utils.models import SoftDeletableModel
from django.utils import timezone
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
import os




class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		"""
		Cria e salva um usuario.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email), 
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		"""
		Cria e salva um super usuario.
		"""
		user = self.create_user(
			email,
			password=password,
		)
		user.username=email
		user.is_admin = True
		user.is_active = True
		user.save(using=self._db)
		return user


class Usuario(AbstractBaseUser):
	nome = models.CharField(max_length=45, null=True, blank=True)
	sobrenome = models.CharField(max_length=45, null=True, blank=True)
	nomecompleto = models.CharField(max_length=100, null=True, blank=True)
	email = models.CharField('email', max_length=75, unique=True, default='')
	cpf = models.CharField(max_length=14, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	username = models.CharField(max_length=45, null=True, blank=True)
	token = models.CharField(max_length=100, null=True, blank=True)
	registration_id = models.CharField(max_length=100, null=True, blank=True)
	objects = UserManager()

	USERNAME_FIELD = 'email'

	def get_full_name(self):
		# The user is identified by their email address
		return self.nome

	def get_first_name(self):
		# The user is identified by their email address
		if self.nome:
			return self.nome.split(' ', 1)[0]
		else:
			return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.nome

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	def __str__(self):
		return self.email


class BestPraticesModel(SoftDeletableModel):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Seguradora(BestPraticesModel):
    name = models.CharField(verbose_name='Nome', max_length=254)

    class Meta:
        verbose_name = "Seguradora"

    def __str__(self):
        return '{}'.format(self.name)


class SeguradoraParametro(BestPraticesModel):
	a_partir = models.DecimalField(default='0', verbose_name='A partir', max_digits=14, decimal_places=2, blank=True, null=True)
	ate = models.DecimalField(default='0', verbose_name='Até', max_digits=14, decimal_places=2, blank=True, null=True)
	is_apartir = models.BooleanField(verbose_name='A partir')
	is_ate = models.BooleanField(verbose_name='Até')	
	seguradora = models.ForeignKey(Seguradora, on_delete=models.DO_NOTHING, verbose_name='Seguradora', blank=True, null=True)
	taxa_seguro = models.DecimalField(verbose_name='Taxa do Seguro', max_digits=14, decimal_places=2, blank=True, null=True)

    # is_apartir caso seja TRUE irá desconsiderar o campo 
    # até na leitura e o campo is_ate caso seja TRUE irá 
    # desconsiderar o campo a_partir

	class Meta:
		verbose_name = "Seguradora Paramentro"

	def __str__(self):
		return '{} - R$: {} - R$: {}'.format(self.seguradora, self.a_partir, self.ate)


class Pedido(BestPraticesModel):
	usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
	valor_bike = models.DecimalField(verbose_name='A partir', max_digits=14, decimal_places=2, blank=True, null=True)
	is_atendido = models.BooleanField(verbose_name='É atendido ?', default=False)

	class Meta:
		verbose_name = "Pedido"

	def __str__(self):
		return 'R$: {}'.format(self.valor_bike)


class Proposta(BestPraticesModel):
	usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
	seguradora = models.ForeignKey(Seguradora, on_delete=models.DO_NOTHING, verbose_name='Seguradora', blank=True, null=True)
	preco_seguro = models.DecimalField(verbose_name='Preço do Seguro', max_digits=14, decimal_places=2, blank=True, null=True)
	pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, blank=True, null=True)

	class Meta:
		verbose_name = "Proposta"

	def __str__(self):
		return '{} - R$: {}'.format(self.seguradora, self.preco_seguro)
