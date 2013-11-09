from django.forms import ModelForm
from search.models import Comment, Question, Information, GoodPractice, Person, Project, Event
from search.widgets import *

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'tags']
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TagInput()
        self.fields['tags'].help_text = None

class QuestionForm(ModelForm):
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

class EditInformationForm(ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'text']

class EditCommentForm(ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'text', 'tags']

class EditGoodPracticeForm(ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'text']

class EditPersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ['title', 'name', 'headline', 'about', 'photo', 'website',
                  'email']

class EditProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'text', 'contact']

class EditEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'text', 'contact']
