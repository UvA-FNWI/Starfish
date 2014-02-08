from django.shortcuts import render, get_object_or_404, redirect, \
    render_to_response
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.core import serializers
from django.core.mail import EmailMultiAlternatives

from search.models import *
from search.forms import *
from search.widgets import *
from search import utils
from search import retrieval

import itertools
import re
import json
import logging

from pprint import pprint
from urllib import quote

from steep.settings import SEARCH_SETTINGS, LOGIN_REDIRECT_URL, HOSTNAME, ITEM_TYPES

MAX_AUTOCOMPLETE = 5
logger = logging.getLogger('search')

from functools import wraps

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


def editcontent(request, pk):
    item = get_object_or_404(Items, pk=pk)
    form = EditInformationForm(instance=item.downcast())
    context = {'form', form}
    return render(request, 'edit.html', context)


def person(request, pk):
    person = get_object_or_404(Person, id=pk)

    context = sorted_tags(person.tags.all())
    context['person'] = person
    context['syntax'] = SEARCH_SETTINGS['syntax'],
    context['next'] = person.get_absolute_url()
    return render(request, 'person.html', context)


class InformationView(generic.DetailView):
    model = Information
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InformationView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        context['next'] = self.object.get_absolute_url()
        context['search'] = None

        # Fetch tags and split them into categories
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
        context['next'] = self.object.get_absolute_url()

        return context


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProjectView, self).get_context_data(**kwargs)
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
        context['next'] = self.object.get_absolute_url()

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
        context['next'] = self.object.get_absolute_url()
        context['form'] = CommentForm(initial={'item_type': self.object.type,
                                               'item_id': self.object.id})
        return context

class GlossaryView(generic.DetailView):
    model = Glossary
    template_name = 'glossary.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GlossaryView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['syntax'] = SEARCH_SETTINGS['syntax']
        context['next'] = self.object.get_absolute_url()
        context['information'] = context['glossary']

        try:
            # Fetch tag that is exlained by this
            tag = Tag.objects.get(glossary=context['object'])
        except (Tag.DoesNotExist, Tag.MultipleObjectsReturned):
            context['search'] = None
        else:
            context['search'] = tag
            aliases = list(Tag.objects.filter(alias_of=tag))
            if len(aliases) > 0:
                context['aliases'] = ', '.join([alias.handle for alias in aliases])
            else:
                context['aliases'] = None

        # Fetch tags and split them into categories
        context = dict(context.items() +
                       sorted_tags(self.object.tags.all()).items())
        return context

def login_user(request):
    username = password = redirect = ''
    state = 'Not logged in'
    if request.method == "POST" and request.is_ajax():
        username = request.POST['username']
        password = request.POST['password']
        redirect = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            state = 'Logged in'
            login(request, user)

            # Check if redirecturl valid
            if '//' in redirect and re.match(r'[^\?]*//', redirect):
                redirect = LOGIN_REDIRECT_URL
            data = json.dumps({'success': True,
                               'redirect': redirect })
        else:
            data = json.dumps({'success': False,
                               'redirect': redirect })
        return HttpResponse(data, mimetype='application/json')
    return HttpResponseBadRequest()


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def cast_vote(request):
    # TODO explicitly define upvotes and downvotes
    # TODO something about not upvoting your own comments
    if request.method == "POST" and request.is_ajax():
        model_type = request.POST.get("model",None)
        model_id = request.POST.get("id", None)
        vote = request.POST.get("vote", None)
        if model_type is None or model_id is None or vote is None:
            return HttpResponseBadRequest();

        if request.user.is_authenticated():
            model = get_model_by_sub_id(model_type, int(model_id))
            user = Person.objects.get(user=request.user)
            if int(vote) == 1:
                if not model.upvoters.filter(pk=user.pk).exists():
                    if model.downvoters.filter(pk=user.pk).exists():
                        model.downvoters.remove(user)
                    else:
                        model.upvoters.add(user)
                else:
                    return HttpResponse('You can only vote once.',status=403)
            else:
                if not model.downvoters.filter(pk=user.pk).exists():
                    if model.upvoters.filter(pk=user.pk).exists():
                        model.upvoters.remove(user)
                    else:
                        model.downvoters.add(user)
                else:
                    return HttpResponse('You can only vote once.',status=403)
            model.save()
            return HttpResponse()
        else:
            return HttpResponse('You need to login first.', status=401)
    else:
        return HttpResponseBadRequest();

def loadquestionform(request):
    if request.method == "GET":
        if not request.user.is_authenticated():
            return HttpResponse('You need to login first.', status=401)
        item_type = request.GET.get('model', '')
        item_id = int(request.GET.get('id', ''))
        item = get_model_by_sub_id(item_type, item_id)

        logger.debug("initial questionform")
        questionform = QuestionForm(initial={'item_type': item_type,
                                             'item_id': item_id})
        return render(request, 'askquestion.html',
                      {'form': questionform,
                       'syntax': SEARCH_SETTINGS['syntax']})
    return HttpResponseBadRequest()

def submitquestion(request):
    if request.method == "POST":
        if request.is_ajax():
            questionform = QuestionForm(request.POST)
            logger.debug("request is POST")
            if questionform.is_valid():
                logger.debug('questionform valid')
                item_type = questionform.cleaned_data['item_type']
                item_id = questionform.cleaned_data['item_id']
                item = get_model_by_sub_id(item_type, item_id)

                question = questionform.save(commit=False)
                try:
                    question.author = request.user.person
                except Person.DoesNotExist:
                    # TODO Present message to the user explaining that somehow he
                    # is not linked to a person object.
                    return HttpResponseNotFound()
                logger.debug("Question submitted by user '{}'".format(request.user))
                question.save()
                questionform.save_m2m()

                if item:
                    item.links.add(question)
                    question.links.add(item)
                data = json.dumps({'success': True,
                                   'redirect': question.get_absolute_url() })

                # Send email
                text_content = question.text
                html_content = ("<h3><a href='http://" + HOSTNAME +
                                question.get_absolute_url() + "'>" +
                                question.title + "</a></h3><p><i>by "+
                                question.author.name + "</i></p>" + question.text)
                subject = "Starfish question: " + question.title
                from_email = "notifications@" + HOSTNAME
                to = ["N.Brouwer-Zupancic@uva.nl"]
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             to)
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)
            else:
                logger.debug("questionform invalid")
                data = json.dumps({'success': False,
                                   'errors': dict([(k, [unicode(e) for e in v])
                                   for k,v in questionform.errors.items()])})
            return HttpResponse(data, mimetype='application/json')
    return HttpResponseBadRequest()


def comment(request):
    if not request.user.is_authenticated():
        return HttpResponse('You need to login first.', status=401)
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            item_type = commentform.cleaned_data['item_type']
            item_id = commentform.cleaned_data['item_id']
            item = get_model_by_sub_id(item_type, item_id)
            if not item:
                logger.error("No item found for given type {} and id {}".
                             format(item_type, item_id))

            comment = commentform.save(commit=False)
            try:
                comment.author = request.user.person
            except Person.DoesNotExist:
                # TODO Present message to the user explaining that somehow he
                # is not linked to a person object.
                return HttpResponseNotFound(
                    "The user is not linked to a person profile."
                )
            comment.save()
            commentform.save_m2m()

            logger.debug("Comment by user '{}' on item {}/{}".
                         format(request.user, item_type, item_id))
            item.comments.add(comment)
            if item_type == 'Q':
                item.tags.add(*comment.tags.all())
            return HttpResponse("Comment added")
        else:
            return HttpResponseBadRequest("Input was not valid");
    else:
        return HttpResponseBadRequest("This HTTP method is not supported.");

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
            # Suggestions based on titles
            # We have to query by type because TextItem is abstract
            objs = list(GoodPractice.objects.filter(title__istartswith=string))
            objs += list(Question.objects.filter(title__istartswith=string))
            objs += list(Information.objects.filter(title__istartswith=string))
            objs += list(Project.objects.filter(title__istartswith=string))
            objs += list(Event.objects.filter(title__istartswith=string))
            titles = [i.title for i in objs]
            literals = titles + [string]

        matches = []
        for tag in tags:
            matches.append(syntax['TAG'] + tag.handle)
        for person in persons:
            matches.append(syntax['PERSON'] + person.handle)
        for literal in literals:
            matches.append(syntax['LITERAL'] + literal + syntax['LITERAL'])
        return HttpResponse(json.dumps(matches),
                            content_type="application/json")
    else:
        return HttpResponse("[]", content_type="application/json")


def tag(request, handle):
    symb = quote(SEARCH_SETTINGS['syntax']['TAG'])
    try:
        tag = Tag.objects.get(handle__iexact=handle)
    except:
        return redirect('/?q='+ symb + handle)
    if tag.glossary is not None:
        return redirect(tag.glossary.get_absolute_url())
    elif tag.alias_of is not None and tag.alias_of.glossary is not None:
        return redirect(tag.alias_of.glossary.get_absolute_url())
    else:
        return redirect('/?q=' + symb + handle)

def browse(request):
    items = Item.objects.all()

    results = {}

    # Ensure unique results
    for item in items:
        # Append the dict_format representation of the item to the results
        results[item.id] = item.dict_format()
    results = results.values()

    def compare(item1, item2):
        ''' Sort based on scope, featured, mentioned in query,
        score, date '''
        if item1['score'] != item2['score']:
            return int(round(item1['score'] - item2['score']))
        if item1['featured'] ^ item2['featured']:
            return int(round(item1['featured'] - item2['featured']))
        return int(round(item1['create_date'] < item2['create_date']) -
                   (item1['create_date'] > item2['create_date']))

        # TODO scope
        # TODO mentioned in query
        # TODO separate persons?

    results_by_type = dict()
    for result in results:
        try:
            results_by_type[''.join(result['type'].split())].append(result)
        except KeyError:
            results_by_type[''.join(result['type'].split())] = [result]

    for l in results_by_type.values():
        l.sort(compare)

    # Find first type that has nonzero value count
    for type_id, type_name in ITEM_TYPES:
        if type_name.replace(" ", "") in results_by_type:
            first_active = type_name.replace(" ", "").lower()
            break
    else:
        first_active = ""

    return render(request, 'browse.html', {
        'results': results_by_type,
        'cols': 1,
        'first_active': first_active,
    })

def search(request):
    string = request.GET.get('q', '')
    if len(string) > 0:
        query, dym_query, dym_query_raw, results, special = retrieval.retrieve(
                string, True)
        def compare(item1, item2):
            ''' Sort based on scope, featured, mentioned in query,
            score, date '''
            if item1['score'] != item2['score']:
                return int(round(item1['score'] - item2['score']))
            if item1['featured'] ^ item2['featured']:
                return int(round(item1['featured'] - item2['featured']))
            return int(round(item1['create_date'] < item2['create_date']) -
                       (item1['create_date'] > item2['create_date']))

            # TODO scope
            # TODO mentioned in query
            # TODO separate persons?

        results_by_type = dict()
        for result in results:
            try:
                results_by_type[''.join(result['type'].split())].append(result)
            except KeyError:
                results_by_type[''.join(result['type'].split())] = [result]

        for l in results_by_type.values():
            l.sort(compare)

        tag_tokens, person_tokens, literal_tokens = utils.parse_query(query)

        # Extract the tokens, discard location information
        tag_tokens = map(lambda x: x[0], tag_tokens)
        person_tokens = map(lambda x: x[0], person_tokens)
        literal_tokens = map(lambda x: x[0], literal_tokens)

        tag_tokens = retrieval.get_synonyms(tag_tokens)
        q_tags = Tag.objects.filter(handle__in=tag_tokens)

        q_types = set()
        for tag in q_tags:
            q_types.add(tag.type)

        # Find first type that has nonzero value count
        for type_id, type_name in ITEM_TYPES:
            if type_name.replace(" ", "") in results_by_type:
                first_active = type_name.replace(" ", "").lower()
                break
        else:
            first_active = ""

        # Sort tags by type and alphabetically
        for l in results_by_type.values():
            for result in l:
                t_sorted = sorted_tags(result['tags']).values()
                # Don't show 'irrelevant' tags
                filtered = []
                for by_type in t_sorted:
                    filtered.append(filter(lambda x:
                                           (x['type'] not in q_types or
                                            x['handle'] in tag_tokens),
                                           by_type))
                trimmed = []
                for t in filtered:
                    if len(t) > 1:
                        # TODO: pick one
                        handle = str('+' + str(len(t) - 1) +
                                     ' ' + t[0]['type_name'])
                        dom_id = str(result['id']) + t[0]['type']
                        trimmed.append([t[0],
                                        {'handle': handle,
                                         'more': t[1:],
                                         'dom_id': dom_id}])
                    else:
                        trimmed.append(t)
                result['tags'] = itertools.chain(*trimmed)
    else:
        query = ""
        dym_query = query
        dym_query_raw = query
        results_by_type = {}
        special = None
        first_active = ""

    return render(request, 'index.html', {
        'special': special,
        'results': results_by_type,
        'syntax': SEARCH_SETTINGS['syntax'],
        'query': query,
        'dym_query': dym_query,
        'dym_query_raw': dym_query_raw,
        'cols': 1,      # replaces len(results_by_type)
        'first_active': first_active
    })


def search_list(request):
    string = request.GET.get('q', '')
    if len(string) > 0:
        query, dym_query, dym_query_raw, results, special = retrieval.retrieve(
                string, True)

        def compare(item1, item2):
            """Sort based on scope, featured, mentioned in query, score, date
            """
            if item1['score'] != item2['score']:
                return int(round(item1['score'] - item2['score']))
            if item1['featured'] ^ item2['featured']:
                return int(round(item1['featured'] - item2['featured']))
            return int(round(item1['create_date'] < item2['create_date']) -
                       (item1['create_date'] > item2['create_date']))

            # TODO scope
            # TODO mentioned in query
            # TODO separate persons?

        results.sort(compare)

        tag_tokens, person_tokens, literal_tokens = utils.parse_query(query)

        # Extract the tokens, discard location information
        tag_tokens = map(lambda x: x[0], tag_tokens)
        person_tokens = map(lambda x: x[0], person_tokens)
        literal_tokens = map(lambda x: x[0], literal_tokens)

        tag_tokens = retrieval.get_synonyms(tag_tokens)
        q_tags = Tag.objects.filter(handle__in=tag_tokens)

        q_types = set()
        for tag in q_tags:
            q_types.add(tag.type)

        # Sort tags by type and alphabetically
        for result in results:
            t_sorted = sorted_tags(result['tags']).values()
            # Don't show 'irrelevant' tags
            filtered = []
            for by_type in t_sorted:
                filtered.append(filter(lambda x: (x['type'] not in q_types or
                                                  x['handle'] in tag_tokens),
                                       by_type))
            trimmed = []
            for t in filtered:
                if len(t) > 1:
                    # TODO: pick one
                    handle = '+' + str(len(t) - 1) + ' ' + t[0]['type_name']
                    dom_id = str(result['id']) + t[0]['type']
                    trimmed.append([t[0],
                                    {'handle': handle,
                                     'more': t[1:],
                                     'dom_id': dom_id}])
                else:
                    trimmed.append(t)
            result['tags'] = itertools.chain(*trimmed)

    else:
        query = ""
        dym_query = query
        dym_query_raw = query
        results = []
        special = None

    return render(request, 'index_list.html',
                  {'special': special,
                   'results': results,
                   'syntax': SEARCH_SETTINGS['syntax'],
                   'query': query,
                   'dym_query': dym_query,
                   'dym_query_raw': dym_query_raw})


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
    elif model_type == 'S':
        model = Glossary.objects.get(pk=model_id)
    return model
