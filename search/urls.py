from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
        url(r'^$', views.search, name='index'),
        url(r'^autocomplete$', views.autocomplete, name='autocomplete'),
        url(r'^search', views.search, name='search'),
        )
