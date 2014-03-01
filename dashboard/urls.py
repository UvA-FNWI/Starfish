from django.conf.urls import patterns, url, include
from dashboard import views

urlpatterns = \
    patterns('',
             url(r'$',
                 views.edit_me, name='edit_me'),
             url(r'me$',
                 views.edit_me, name='edit_me'))
