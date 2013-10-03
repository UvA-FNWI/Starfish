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


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Info.objects.order_by('-pub_date')[:10]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        return context


class PersonView(generic.DetailView):
    model = Person
    template_name = 'person.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PersonView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        return context


class InfoView(generic.DetailView):
    model = Info
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InfoView, self).get_context_data(**kwargs)
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
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        # TODO get current author, do not save if not present
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.author = Person.objects.filter(name__istartswith="Nat")[0]
            print comment.author.name
            comment.save()
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
    return render(request, 'index.html', {'results': results,
                                          'query': query})
