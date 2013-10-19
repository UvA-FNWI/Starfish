from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from search.models import *
from search.forms import *
from search.widgets import *
from search import utils
from search import retrieval

import itertools

import json

from steep.settings import SEARCH_SETTINGS

MAX_AUTOCOMPLETE = 5


def sorted_tags(tags):
    p, t, c, o = [], [], [], []

    try:
        for tag in tags:
            if tag['type'] == "P":
                p.append(tag)
            elif tag['type'] == "T":
                t.append(tag)
            elif tag['type'] == "C":
                c.append(tag)
            elif tag['type'] == "O":
                o.append(tag)
        p.sort(key=lambda x: x['handle'])
        t.sort(key=lambda x: x['handle'])
        c.sort(key=lambda x: x['handle'])
        o.sort(key=lambda x: x['handle'])

    except TypeError:
        for tag in tags:
            if tag.type == "P":
                p.append(tag)
            elif tag.type == "T":
                t.append(tag)
            elif tag.type == "C":
                c.append(tag)
            elif tag.type == "O":
                o.append(tag)
        p.sort(key=lambda x: x.handle)
        t.sort(key=lambda x: x.handle)
        c.sort(key=lambda x: x.handle)
        o.sort(key=lambda x: x.handle)

    return {'p': p, 't': t, 'c': c, 'o': o}


def person(request, pk):
    person = Person.objects.get(id=pk)

    context = sorted_tags(person.tags.all())
    context['person'] = person
    context['syntax'] = SEARCH_SETTINGS['syntax'],
    return render(request, 'person.html', context)


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
        print sorted_tags(self.object.tags.all())
        context = dict(context.items() +
                sorted_tags(self.object.tags.all()).items())
        return context


class GoodPracticeView(InformationView):
    model = GoodPractice

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GoodPracticeView, self).get_context_data(**kwargs)
        context['information'] = context['goodpractice']
        return context


class EventView(generic.DetailView):
    model = Event
    template_name = 'event.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EventView, self).get_context_data(**kwargs)
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
        return context


def vote(request, model_type, model_id, vote):
    # TODO check if user is logged in
    user = Person.objects.filter(name__istartswith="Nat")[0]
    model = get_model_by_sub_id(model_type, int(model_id))
    print model
    if not model.voters.filter(pk=user.pk).exists():
        model.upvotes += int(vote)
        models.voters.add(user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def askquestion(request):
    item_type = request.GET.get('type', '')
    item_id = int(request.GET.get('id', ''))

    if request.method == "POST":
        questionform = QuestionForm(request.POST)
    else:
        questionform = QuestionForm()

    return render(request, 'askquestion.html', {'form': questionform,
                                                'type': item_type,
                                                'id': item_id})

def submitquestion(request):
    item_type = request.GET.get('type', '')
    item_id = request.GET.get('id', '')

    if request.method == "POST":
        questionform = QuestionForm(request.POST)

        if questionform.is_valid():
            question = questionform.save(commit=False)
            # TODO get current author, do not save if not present
            print request.user
            question.author = Person.objects.filter(name__istartswith="Nat")[0]
            question.save()
            questionform.save_m2m()

            item = get_model_by_sub_id(item_type, int(item_id))
            if item:
                item.links.add(question)
                item.tags.add(None)

            # TODO redirect to resulting question
    else:
        #commentform = CommentForm()
        #commentform.fields['tags'].widget = TagInput()
        #commentform.fields['tags'].help_text = None
        pass
    return render(request, 'askquestion.html', {'form': commentform})

def comment(request):
    item_type = request.GET.get('type', '')
    item_id = int(request.GET.get('id', ''))

    if request.method == "POST":
        commentform = CommentForm(request.POST)

        if commentform.is_valid():
            comment = commentform.save(commit=False)
            # TODO get current author, do not save if not present
            print request.user
            comment.author = Person.objects.filter(name__istartswith="Nat")[0]
            comment.save()
            commentform.save_m2m()

            if item_type == 'Q':
                question = Question.objects.get(pk=item_id)
                question.comments.add(comment)
                question.tags.add(*comment.tags.all())
                print 'Added tags'

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

    # Sort tags by type and alphabetically
    for result in results:
        result['tags'] = itertools.chain(*sorted_tags(result['tags']).values())

    return render(request, 'index.html', {
        'results': results,
        'syntax': SEARCH_SETTINGS['syntax'],
        'query': query
    })

def get_model_by_sub_id(model_type, model_id):
    ''' We know the model_id and type, but the id
    identifies it among its equals.. and not all models!
    '''
    model = None
    if model_type == 'P':
        model = Person.objects.get(pk=model_id)
    elif model_type == 'G':
        model = GoodPractice.objects.get(pk=model_id)
    elif model_type == 'I':
        model = Information.objects.get(pk=model_id)
    elif model_type == 'R':
        model = Project.objects.get(pk=model_id)
    elif model_type == 'E':
        model = Event.objects.get(pk=model_id)
    elif model_type == 'Q':
        model = Question.objects.get(pk=model_id)
    elif model_type == 'C':
        model = Comment.objects.get(pk=model_id)
    return model
