from django.forms import ModelForm
from search.models import Comment, Question
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
