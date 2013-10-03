from django.forms import ModelForm
from search.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'tags']
