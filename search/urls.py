from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
        url(r'^$', views.search, name='index'),
        url(r'^autocomplete$', views.autocomplete, name='autocomplete'),
        url(r'^search', views.search, name='search'),
        url(r'^person/(?P<pk>\d+)/$', views.person, name='person'),
        url(r'^information/(?P<pk>\d+)/$', views.InformationView.as_view(), name='info'),
        url(r'^question/(?P<pk>\d+)/$', views.QuestionView.as_view(), name='question'),
        url(r'^comment$', views.comment, name='comment'),
        )
