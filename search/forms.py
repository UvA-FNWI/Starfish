from django.forms import ModelForm, CharField, IntegerField, HiddenInput
from search.models import Comment, Question, Information, GoodPractice, \
    Person, Project, Event, Glossary, Community
from search.widgets import TagInput
from bootstrap3_datetime.widgets import DateTimePicker


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

class DashboardForm(ModelForm):

    def __init__(self, *args, **kwargs):
        if "communities" in kwargs:
            communities = kwargs["communities"]
            del kwargs["communities"]
        else:
            communities = Community.objects
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = TagInput()
        self.fields['tags'].help_text = None
        if 'communities' in self.fields:
            self.fields['communities'].queryset = communities
        if 'date' in self.fields:
            self.fields['date'].widget = \
                DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                        "pickSeconds": False})


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
        model = Question
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
        model = Glossary
        fields = ['title', 'text', 'tags', 'author', 'links', 'communities']
