from django.conf.urls import patterns, url, include

from search import views, apis

urlpatterns = \
    patterns('',
             url(r'^$',
                 views.search, name='index'),
             url(r'^autocomplete$',
                 views.autocomplete, name='autocomplete'),
             url(r'^search',
                 views.search_list, name='search'),
             url(r'^browse',
                 views.browse, name='browse'),
             url(r'^dashboard/$',
                 views.dashboard, name='dashboard'),

             url(r'^tag/(?P<handle>.+)/$',
                 views.tag, name='tag'),
             url(r'^person/(?P<pk>\d+)/$',
                 views.person, name='person'),

             # Infos
             url(r'^information/(?P<pk>\d+)/$',
                 views.InformationView.as_view(), name='info'),
             url(r'^event/(?P<pk>\d+)/$',
                 views.EventView.as_view(), name='info'),
             url(r'^project/(?P<pk>\d+)/$',
                 views.ProjectView.as_view(), name='info'),
             url(r'^goodpractice/(?P<pk>\d+)/$',
                 views.GoodPracticeView.as_view(), name='goodpractice'),
             url(r'^glossary/(?P<pk>\d+)/$',
                 views.GlossaryView.as_view(), name='glossary'),
             url(r'^question/(?P<pk>\d+)/$',
                 views.QuestionView.as_view(), name='question'),

             # Forms
             url(r'^dashboard/information/(?P<pk>\d+)/$',
                 views.InformationForm.as_view(), name='info_edit'),
             url(r'^dashboard/event/(?P<pk>\d+)/$',
                 views.EventForm.as_view(), name='info_edit'),
             url(r'^dashboard/project/(?P<pk>\d+)/$',
                 views.ProjectForm.as_view(), name='info_edit'),
             url(r'^dashboard/goodpractice/(?P<pk>\d+)/$',
                 views.GoodPracticeForm.as_view(), name='goodpractice_edit'),
             url(r'^dashboard/glossary/(?P<pk>\d+)/$',
                 views.GlossaryForm.as_view(), name='glossary_edit'),
             url(r'^dashboard/question/(?P<pk>\d+)/$',
                 views.QuestionForm.as_view(), name='question_edit'),

             url(r'^loadquestionform$',
                 views.loadquestionform, name='loadquestionform'),
             url(r'^submitquestion$',
                 views.submitquestion, name='submitquestion'),
             url(r'^comment$',
                 views.comment, name='comment'),
             url(r'^vote$',
                 views.cast_vote, name='cast_vote'),
             url(r'^api/comment$',
                 apis.comment, name='api_comment'),

             url(r'^login',
                 views.login_user, name='login'),
             url(r'^logout',
                 views.logout_user, name='logout'),
             )
