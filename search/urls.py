from django.conf.urls import patterns, url

from search import views

urlpatterns = patterns('',
        url(r'^$', views.search, name='index'),
        url(r'^autocomplete$', views.autocomplete, name='autocomplete'),
        url(r'^search', views.search, name='search'),
        url(r'^tag/(?P<handle>.+)/$', views.tag, name='tag'),
        url(r'^person/(?P<pk>\d+)/$', views.person, name='person'),
        url(r'^information/(?P<pk>\d+)/$', views.InformationView.as_view(), name='info'),
        url(r'^goodpractice/(?P<pk>\d+)/$', views.GoodPracticeView.as_view(), name='goodpractice'),
        url(r'^question/(?P<pk>\d+)/$', views.QuestionView.as_view(), name='question'),
        url(r'^comment$', views.comment, name='comment'),
        )
