from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from search.models import *
from search.forms import *
from search import utils
from search import retrieval


import json

from steep.settings import SEARCH_SETTINGS

MAX_AUTOCOMPLETE = 5

class PersonView(generic.DetailView):
    model = Person
    template_name = 'person.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PersonView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        return context


class InformationView(generic.DetailView):
    model = Information
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InformationView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        return context


class QuestionView(generic.DetailView):
    model = Question
    template_name = 'question.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuestionView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        context['form'] = CommentForm()
        return context


def comment(request):
    item_type = request.GET.get('type', '')
    item_id = request.GET.get('id', '')

    if request.method == "POST":
        commentform = CommentForm(request.POST)

        if commentform.is_valid():
            if item_type == 'Q':
                item = Question.objects.get(pk=int(item_id))

            comment = commentform.save(commit=False)
            # TODO get current author, do not save if not present
            print request.user
            comment.author = Person.objects.filter(name__istartswith="Nat")[0]
            comment.save()
            commentform.save_m2m()
            item.comments.add(comment)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        commentform = CommentForm()


    return render(request, 'question.html', {'form': commentform})


def autocomplete(request):
    string = request.GET.get('q', '')
    if len(string) > 0:
        syntax = SEARCH_SETTINGS['syntax']
        if string[0] == syntax['TAG']:
            tags = Tag.objects.filter(handle__istartswith=string[1:])
            persons = []
            literals = []
        elif string[0] == syntax['PERSON']:
            tags = []
            persons = Person.objects.filter(name__istartswith=string[1:])
            literals = []
        elif string[0] == syntax['LITERAL']:
            tags = []
            persons = []
            literals = [string[1:]]
        else:
            tags = Tag.objects.filter(handle__istartswith=string)
            persons = Person.objects.filter(name__istartswith=string)
            literals = [string]

        matches = []
        for tag in tags:
            matches.append(syntax['TAG']+tag.handle)
        for person in persons:
            matches.append(syntax['PERSON']+person.handle)
        for literal in literals:
            matches.append(syntax['LITERAL']+literal+syntax['LITERAL'])
        return HttpResponse(json.dumps(matches),
            content_type="application/json")
    else:
        return HttpResponse("[]",content_type="application/json")

def search(request):
    string = request.GET.get('q', '')
    query, results = retrieval.retrieve(string)
    return render(request, 'index.html', {
        'results': results,
        'syntax': SEARCH_SETTINGS['syntax'],
        'query': query
    })
