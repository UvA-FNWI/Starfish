from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse

from search.models import *
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

class PersonView(generic.DetailView):
    model = Person
    template_name = 'person.html'

class InfoView(generic.DetailView):
    model = Info
    template_name = 'info.html'

class QuestionView(generic.DetailView):
    model = Question
    template_name = 'question.html'

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
