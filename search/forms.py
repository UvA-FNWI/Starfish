from django.forms import ModelForm, CharField, IntegerField, HiddenInput
from search.models import Comment, Question, Information, GoodPractice, \
    Person, Project, Event
from search.widgets import *


class CommentForm(ModelForm):
    item_type = CharField(widget=HiddenInput())
    item_id = IntegerField(widget=HiddenInput())

    class Meta:
        model = Comment
        fields = ['text', 'tags']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TagInput()
        self.fields['tags'].help_text = None


class QuestionForm(ModelForm):
    item_type = CharField(widget=HiddenInput())
    item_id = IntegerField(widget=HiddenInput())

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TagInput()
        self.fields['tags'].help_text = None


# TODO somehow generalize?
#class EditForm(ModelForm):
#    class Meta:
#        model = None
#        fields = []
#    def __init__(self, *args, **kwargs):
#        self.Meta.model = kwargs['model']
#        self.Meta.fields = kwargs['fields']
#        super(EditForm, self).__init__(*args, **kwargs)


class DashboardForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TagInput()
        self.fields['tags'].help_text = None


class EditInformationForm(DashboardForm):
    class Meta:
        model = Information
        fields = ['title', 'text', 'links', 'author', 'communities', 'tags',
                  'links']


class EditCommentForm(DashboardForm):
    class Meta:
        model = Information
        fields = ['title', 'text', 'tags']


class EditGoodPracticeForm(DashboardForm):
    class Meta:
        model = GoodPractice
        fields = ['title', 'text', 'links', 'author', 'communities', 'tags',
                  'links']


class EditQuestionForm(DashboardForm):
    class Meta:
        model = GoodPractice
        fields = ['title', 'text', 'links', 'author', 'communities', 'tags',
                  'links']


class EditPersonForm(DashboardForm):
    class Meta:
        model = Person
        fields = ['title', 'name', 'headline', 'about', 'photo', 'website',
                  'email', 'communities']


class EditProjectForm(DashboardForm):
    class Meta:
        model = Project
        fields = ['title', 'text', 'contact', 'author', 'communities', 'links',
                  'tags']


class EditEventForm(DashboardForm):
    class Meta:
        model = Event
        fields = ['title', 'text', 'contact', 'author', 'communities', 'links',
                  'tags', 'date']


class EditGlossaryForm(DashboardForm):
    class Meta:
        model = Event
        fields = ['title', 'text', 'tags', 'links', 'communities']
