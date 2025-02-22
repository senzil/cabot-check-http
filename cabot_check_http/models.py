from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django import forms
from django.template import Context, Template

from cabot3.cabotapp.models import StatusCheckResult, StatusCheck

from os import environ as env
import re
import subprocess
import requests
import logging


class HttpStatusCheckForm(forms.Form):
    # HTTP checks
    endpoint = forms.CharField(
        help_text='HTTP(S) endpoint to poll.',
        widget = forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': 'https://www.arachnys.com',
            }),
    )
    username = forms.CharField(
        help_text='Basic auth username.',
        required=False,
        widget = forms.TextInput(attrs={
            'style': 'width: 30%',
            }),
    )
    password = forms.CharField(
        help_text='Basic auth password.',
        required=False,
        widget = forms.TextInput(attrs={
            'style': 'width: 30%',
            }),
    )
    text_match = forms.CharField(
        help_text='Regex to match against source of page.',
        required=False,
        widget = forms.TextInput(attrs={
            'style': 'width: 100%',
            'placeholder': '[Aa]rachnys\s+[Rr]ules',
            }),
    )
    status_code = forms.CharField(
        initial=200,
        help_text='Status code expected from endpoint.',
        required=False,
        widget = forms.TextInput(attrs={
            'style': 'width: 20%',
            'placeholder': '200',
            }),
    )
    timeout = forms.IntegerField(
        initial=30,
        help_text='Time out after this many seconds.',
        required=False,
    )
    verify_ssl_certificate = forms.BooleanField(
        initial=True,
        help_text='Set to false to allow not try to verify ssl certificates (default True)',
        required=False,
    )


class HttpStatusCheck(StatusCheck):
    
    check_name = 'http'
    name = "HTTP Status"
    slug = "cabot_check_http"
    author = "Jonathan Balls"
    version = "0.0.1"
    font_icon = "glyphicon glyphicon-arrow-up"

    config_form = HttpStatusCheckForm

    plugin_variables = [
        'HTTP_USER_AGENT',
    ]

    def _run(self):
        result = StatusCheckResult(status_check=self)

        auth = None
        if self.username or self.password:
            auth = (self.username if self.username is not None else '',
                    self.password if self.password is not None else '')

        try:
            resp = requests.get(
                self.endpoint,
                timeout=self.timeout,
                verify=self.verify_ssl_certificate,
                auth=auth,
                headers={
                    "User-Agent": settings.HTTP_USER_AGENT,
                },
            )
        except requests.RequestException as e:
            result.error = u'Request error occurred: %s' % (e.message,)
            result.succeeded = False
        else:
            if self.status_code and resp.status_code != int(self.status_code):
                result.error = u'Wrong code: got %s (expected %s)' % (
                    resp.status_code, int(self.status_code))
                result.succeeded = False
                result.raw_data = resp.text
            elif self.text_match:
                if not self._check_content_pattern(self.text_match, resp.text):
                    result.error = u'Failed to find match regex /%s/ in response body' % self.text_match
                    result.raw_data = resp.text
                    result.succeeded = False
                else:
                    result.succeeded = True
            else:
                result.succeeded = True
        return result

    def __str__(self):
        return self.name
        
    def description(self, check):
        if check.endpoint:
            return 'Status Code {} from {}'.format(check.status_code, check.endpoint)
        else:
            return 'HTTP Check with no target.'

