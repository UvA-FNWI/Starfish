from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse

from search.models import *
from search import utils
from search import retrieval

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
    try:
        string = request.GET.get('q')
    except:
        return HttpResponse()
    matches = Tag.objects.filter(name__istartswith=string)
    return HttpResponse(matches)


def search(request):
    string = request.GET.get('q', '')
    query, results = retrieval.retrieve(string)
    return render(request, 'index.html', {'results': results,
                                          'query': query})
