from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from datetime import datetime, timedelta
from django.db import IntegrityError, transaction, connection
from django.views.generic import RedirectView, View, UpdateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormMixin
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse)
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from pprint import pprint # print for json or dict
import requests
import threading
from requests.auth import HTTPBasicAuth
import json

'''
	EMAIL THREAD
'''
class EmailThread(threading.Thread):
    def __init__(self,
                 subject,
                 body,
                 from_email,
                 recipient_list,
                 fail_silently,
                 html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject,
                                     self.body,
                                     self.from_email,
                                     self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)

'''
  SMS
'''
class Sms(object):

    def __init__(self, token=settings.SMS_TOKEN):
        self.token = token 
        # Gerar token no linux echo -n conta:senha | base64

    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' %self.token,
            'Accept': 'application/json'
        }


    def send(self, data={}):
        try:
            url = 'https://api-rest.zenvia.com/services/send-sms'
            response = requests.post(url, headers=self.headers(),data=json.dumps(data))
            if 'Error' in response.text:
                raise ValueError('sms is False')
            return True
        except ValueError as e:
            url = "https://api-messaging.movile.com/v1/send-sms"
            payload = "{\"destination\": \"%s\" ,  \"messageText\": \"%s %s\"}" % (data['sendSmsRequest']['to'], data['sendSmsRequest']['from'], data['sendSmsRequest']['msg'])
            headers = {
                'username': "BIURI MARKETPLACE LTDA",
                'authenticationtoken': self.token,
                'content-type': "application/json"
                }

            response = requests.post(url, data=payload, headers=headers)
            if 'errorCode' in response.text:
                return False
            return True

 


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(to, title, body):
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'https://exp.host/--/api/v2/push/send'
    payload = {'to': to, 'title': title,'body': body}
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return json.loads(res.content.decode('utf-8'))