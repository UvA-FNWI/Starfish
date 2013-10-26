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
        url(r'^askquestion$', views.askquestion, name='askquestion'),
        url(r'^submitquestion$', views.submitquestion, name='submitquestion'),
        url(r'^comment$', views.comment, name='comment'),
        url(r'^vote/(?P<model_type>\w)/(?P<model_id>\d+)/(?P<vote>-?\d)$', views.vote, name='vote'),
        url(r'^login', views.login_user, name='login'),
        url(r'^logout', views.logout_user, name='logout'),
        )
