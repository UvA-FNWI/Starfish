from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<info_id>\d+)/$', views.info, name='info'),
        )
