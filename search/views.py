from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from search.models import *
from search.forms import *
from search.widgets import *
from search import utils
from search import retrieval


import json

from steep.settings import SEARCH_SETTINGS

MAX_AUTOCOMPLETE = 5


def person(request, pk):
    person = Person.objects.get(id=pk)
    p, t, c, o = [], [], [], []

    for tag in person.tags.all():
        if tag.type == "P":
            p.append(tag)
        elif tag.type == "T":
            t.append(tag)
        elif tag.type == "C":
            c.append(tag)
        elif tag.type == "O":
            o.append(tag)

    return render(request, 'person.html', {
        'person': person,
        'syntax': SEARCH_SETTINGS['syntax'],
        'p': p,
        't': t,
        'c': c,
        'o': o
    })

class InformationView(generic.DetailView):
    model = Information
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InformationView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']

        # Fetch tag that is exlained by this, if applicable
        infotags = Tag.objects.filter(info=context['object'])
        if len(infotags) > 0:
            context['search'] = infotags[0]
        else:
            context['search'] = None

        # Fetch tags and split them into categories
        p, t, c, o = [], [], [], []
        for tag in self.object.tags.all():
            if tag.type == "P":
                p.append(tag)
            elif tag.type == "T":
                t.append(tag)
            elif tag.type == "C":
                c.append(tag)
            elif tag.type == "O":
                o.append(tag)
        context['p'] = p
        context['t'] = t
        context['c'] = c
        context['o'] = o
        return context

class GoodPracticeView(InformationView):
    model = GoodPractice

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GoodPracticeView, self).get_context_data(**kwargs)
        context['information'] = context['goodpractice']
        return context


class QuestionView(generic.DetailView):
    model = Question
    template_name = 'question.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuestionView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        # Fetch tags and split them into categories
        p, t, c, o = [], [], [], []
        for tag in self.object.tags.all():
            if tag.type == "P":
                p.append(tag)
            elif tag.type == "T":
                t.append(tag)
            elif tag.type == "C":
                c.append(tag)
            elif tag.type == "O":
                o.append(tag)
        context['p'] = p
        context['t'] = t
        context['c'] = c
        context['o'] = o

        context['form'] = CommentForm()
        context['form'].fields['tags'].widget = TagInput()
        context['form'].fields['tags'].help_text = None
        return context


def comment(request):
    item_type = request.GET.get('type', '')
    item_id = request.GET.get('id', '')

    if request.method == "POST":
        commentform = CommentForm(request.POST)
        commentform.fields['tags'].widget = TagInput()
        commentform.fields['tags'].help_text = None

        if commentform.is_valid():
            comment = commentform.save(commit=False)
            # TODO get current author, do not save if not present
            print request.user
            comment.author = Person.objects.filter(name__istartswith="Nat")[0]
            comment.save()
            commentform.save_m2m()

            if item_type == 'Q':
                Question.objects.get(pk=int(item_id)).comments.add(comment)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        commentform = CommentForm()
        commentform.fields['tags'].widget = TagInput()
        commentform.fields['tags'].help_text = None

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
        return HttpResponse("[]", content_type="application/json")

def tag(request, handle):
    try:
        tag = Tag.objects.get(handle__iexact=handle)
    except:
        return redirect('/?q=%23'+handle)
    if tag.info is not None:
        return redirect(tag.info.get_absolute_url())
    else:
        return redirect('/?q=%23'+handle)

def search(request):
    string = request.GET.get('q', '')
    query, results = retrieval.retrieve(string, True)
    results = sorted(results, key=lambda i: i["score"], reverse=True)
    return render(request, 'index.html', {
        'results': results,
        'syntax': SEARCH_SETTINGS['syntax'],
        'query': query
    })
