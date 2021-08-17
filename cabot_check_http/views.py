from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from cabot3.cabotapp.models import StatusCheck
from cabot3.cabotapp.views import (CheckCreateView, CheckUpdateView,
                                  StatusCheckForm, base_widgets)

from .models import HttpStatusCheck



class HttpStatusCheckForm(StatusCheckForm):
    symmetrical_fields = ('service_set', 'instance_set')

    class Meta:
        model = HttpStatusCheck
        fields = (
            'name',
            'endpoint',
            'username',
            'password',
            'text_match',
            'status_code',
            'timeout',
            'verify_ssl_certificate',
            'frequency',
            'importance',
            'active',
            'debounce',
        )
        widgets = dict(**base_widgets)
        widgets.update({
            'endpoint': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': 'https://www.example.org/',
            }),
            'username': forms.TextInput(attrs={
                'style': 'width: 30%',
            }),
            'password': forms.PasswordInput(attrs={
                'style': 'width: 30%',
                # Prevent auto-fill with saved Cabot log-in credentials:
                'autocomplete': 'new-password',
            }),
            'text_match': forms.TextInput(attrs={
                'style': 'width: 100%',
                'placeholder': '[Aa]rachnys\s+[Rr]ules',
            }),
            'status_code': forms.TextInput(attrs={
                'style': 'width: 20%',
                'placeholder': '200',
            }),
        })

    def clean_password(self):
        new_password_value = self.cleaned_data['password']
        if new_password_value == '':
            new_password_value = self.initial.get('password')
        return new_password_value



class HttpCheckCreateView(CheckCreateView):
    model = HttpStatusCheck
    form_class = HttpStatusCheckForm


class HttpCheckUpdateView(CheckUpdateView):
    model = HttpStatusCheck
    form_class = HttpStatusCheckForm



def duplicate_http_check(request, pk):
    pc = StatusCheck.objects.get(pk=pk)
    npk = pc.duplicate()
    return HttpResponseRedirect(reverse('update-http-check', kwargs={'pk': npk}))
