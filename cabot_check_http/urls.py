from django.conf.urls import url

from .views import (HttpCheckCreateView, HttpCheckUpdateView,
                    duplicate_http_check)

urlpatterns = [

     url(r'^httpcheck/create/', 
        view=HttpCheckCreateView.as_view(),
        name='create-http-check'),

     url(r'^httpcheck/update/(?P<pk>\d+)/',
        view=HttpCheckUpdateView.as_view(), 
        name='update-http-check'),

     url(r'^httpcheck/duplicate/(?P<pk>\d+)/',
        view=duplicate_http_check, 
        name='duplicate-http-check'),
]


