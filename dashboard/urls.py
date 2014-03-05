from django.conf.urls import patterns, url, include
from dashboard import views

urlpatterns = \
    patterns('',
             url(r'^$',
                 views.edit_me, name='edit_me'),
             url(r'^me$',
                 views.edit_me, name='edit_me'),
             url(r'^contributions/$',
                 views.contributions, name='contributions'),
             url(r'^information/(?P<pk>\d+)/$',
                 views.InformationForm.as_view(), name='info_edit'),
             url(r'^event/(?P<pk>\d+)/$',
                 views.EventForm.as_view(), name='info_edit'),
             url(r'^project/(?P<pk>\d+)/$',
                 views.ProjectForm.as_view(), name='info_edit'),
             url(r'^goodpractice/(?P<pk>\d+)/$',
                 views.GoodPracticeForm.as_view(), name='goodpractice_edit'),
             url(r'^glossary/(?P<pk>\d+)/$',
                 views.GlossaryForm.as_view(), name='glossary_edit'),
             url(r'^question/(?P<pk>\d+)/$',
                 views.QuestionForm.as_view(), name='question_edit'))
