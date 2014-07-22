from django.shortcuts import render, get_object_or_404, redirect, \
    render_to_response
from django.views import generic
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.core.context_processors import csrf

from search.models import *
from search.forms import *
from search.widgets import *
from search import utils
from search import retrieval

import itertools
import re
import json
import logging
import ldap
import random

from urllib import quote, urlencode
from urllib2 import urlopen, HTTPError

from django.conf import settings

SEARCH_SETTINGS = settings.SEARCH_SETTINGS
LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
HOSTNAME = settings.HOSTNAME
ITEM_TYPES = settings.ITEM_TYPES
IVOAUTH_TOKEN = settings.IVOAUTH_TOKEN
IVOAUTH_URL = settings.IVOAUTH_URL
ADMIN_NOTIFICATION_EMAIL = settings.ADMIN_NOTIFICATION_EMAIL

MAX_AUTOCOMPLETE = 5
logger = logging.getLogger('search')


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
    user_communities = utils.get_user_communities(request.user)

    context = sorted_tags(person.tags.all())
    context['user_communities'] = user_communities
    links = set(person.links.filter(communities__in=user_communities))
    # Remove events that have already passed
    links = set(filter(lambda x: x.type == "E" and not
                       x.downcast().is_past_due, links))

    context['community_links'] = links
    context['person'] = person
    context['syntax'] = SEARCH_SETTINGS['syntax']
    context['next'] = person.get_absolute_url()
    return render(request, 'person.html', context)


class StarfishDetailView(generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super(StarfishDetailView, self).get_context_data(**kwargs)

        user_communities = utils.get_user_communities(self.request.user)
        context['user_communities'] = user_communities

        links = set(self.get_object().links.filter(
            communities__in=user_communities))
        # Remove events that have already passed
        links = set(filter(lambda x: x.type == "E" and not
                           x.downcast().is_past_due, links))
        context['community_links'] = links

        return context


class InformationView(StarfishDetailView):
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
        context = dict((context.items() +
                        sorted_tags(self.object.tags.all()).items()))
        return context


class GoodPracticeView(InformationView):
    model = GoodPractice

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GoodPracticeView, self).get_context_data(**kwargs)
        context['information'] = context['goodpractice']
        return context


class EventView(StarfishDetailView):
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


class ProjectView(StarfishDetailView):
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


class QuestionView(StarfishDetailView):
    model = Question
    template_name = 'question.html'

    def get_context_data(self, *args, **kwargs):
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


class GlossaryView(StarfishDetailView):
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
                context['aliases'] = ', '.join([alias.handle for alias
                                                in aliases])
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
                               'redirect': redirect})
            return HttpResponse(data, mimetype='application/json')
        else:
            data = json.dumps({'success': False,
                               'redirect': redirect})
            return HttpResponseBadRequest(data, mimetype='application/json')
    return HttpResponseBadRequest()


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def ivoauth(request):
    callback_url = str(request.build_absolute_uri("ivoauth/callback")) + \
        "/?ticket={#ticket}"
    post_data = [('token', IVOAUTH_TOKEN), ('callback_url', callback_url)]
    try:
        content = json.loads(urlopen(IVOAUTH_URL + "/ticket",
                             urlencode(post_data)).read())
    except HTTPError:
        logger.error("Invalid url")
        return HttpResponseBadRequest()
    if content["status"] == "success":
        logger.debug("IVO authentication successful")
        return HttpResponseRedirect(IVOAUTH_URL + "/login/" +
                                    content["ticket"])
    else:
        logger.debug("IVO authentication failed")
    return HttpResponseBadRequest()

def ivoauth_debug(request):
    callback_url = str(request.build_absolute_uri("ivoauth/debug_callback")) + \
        "/?ticket={#ticket}"
    post_data = [('token', IVOAUTH_TOKEN), ('callback_url', callback_url)]
    try:
        content = json.loads(urlopen(IVOAUTH_URL + "/ticket",
                             urlencode(post_data)).read())
    except HTTPError:
        logger.error("Invalid url")
        return HttpResponseBadRequest()
    if content["status"] == "success":
        logger.debug("IVO authentication successful")
        return HttpResponseRedirect(IVOAUTH_URL + "/login/" +
                                    content["ticket"])
    else:
        logger.debug("IVO authentication failed")
    return HttpResponseBadRequest()

def ivoauth_debug_callback(request):
    # Retrieve ticket given by ivoauth and use it
    ticket = request.GET.get("ticket", "")
    if not ticket:
        logger.error("no ticket")
    url = IVOAUTH_URL + "/status"
    post_data = [('token', IVOAUTH_TOKEN), ('ticket', ticket)]
    try:
        content = urlopen(url, urlencode(post_data)).read()
    except HTTPError:
        logger.error("Invalid url")
        return HttpResponseBadRequest()

    # Parse response
    content = json.loads(content)
    if content["status"] == "success":
        logger.debug("Authentication successful")
        attributes = content["attributes"]
        external_id = "surfconext/" + attributes["saml:sp:NameID"]["Value"]
        return HttpResponse(external_id)
    return HttpResponseBadRequest()

def ivoauth_callback(request):
    # Retrieve ticket given by ivoauth and use it
    ticket = request.GET.get("ticket", "")
    if not ticket:
        logger.error("no ticket")
    url = IVOAUTH_URL + "/status"
    post_data = [('token', IVOAUTH_TOKEN), ('ticket', ticket)]
    try:
        content = urlopen(url, urlencode(post_data)).read()
    except HTTPError:
        logger.error("Invalid url")
        return HttpResponseBadRequest()

    # Parse response
    content = json.loads(content)
    if content["status"] == "success":
        logger.debug("Authentication successful")
        attributes = content["attributes"]
        external_id = "surfconext/" + attributes["saml:sp:NameID"]["Value"]
        email = attributes["urn:mace:dir:attribute-def:mail"][0]
        person_set = Person.objects.filter(external_id=external_id)
        # If a person with external_id nonexistent, create new person
        if not person_set.exists():
            person = Person()
            person.handle = attributes["urn:mace:dir:attribute-def:uid"][0]
            try:
                surname = attributes["urn:mace:dir:attribute-def:sn"][0]
                first_name = attributes["urn:mace:dir:attribute-def:givenName"][0]
            except KeyError:
                person.name = person.handle
                first_name = ""
                surname = person.handle
                subject = "Surfconext login: missing 'givenName'"
                text_content = "handle: %s\n\n%s" % (person.handle,
                        json.dumps(content))
                from_email = 'warning@'+HOSTNAME
                to = ADMIN_NOTIFICATION_EMAIL
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             to)
                msg.send(fail_silently=True)
            else:
                person.name = first_name + ' ' + surname
            #displayname = attributes["urn:mace:dir:attribute-def:displayName"][0]
            person.email = email
            person.external_id = external_id
            person.save()

            ## Get communities for this person from ivoauth
            # TODO make this a generic method (so other auths can call it)
            # By default, add 'public' community
            person.communities.add(Community.objects.get(pk=1))
            # Get the rest from LDAP
            ldap_obj = ldap.initialize("ldap://ldap1.uva.nl:389")
            search_results = ldap_obj.search_s(
                'ou=Medewerkers,o=Universiteit van Amsterdam,c=NL',
                ldap.SCOPE_ONELEVEL,
                '(&(objectClass=person)(uid=' + person.handle + '))')

            # Expect single search result
            if search_results:
                query, result = search_results[0]
                try:
                    supercommunity = Community.objects.get(name=result['o'][0])
                except Community.DoesNotExist:
                    pass
                else:
                    for community_name in result['ou']:
                        subcommunity = supercommunity.subcommunities.filter(
                            name=community_name)
                        if subcommunity.exists():
                            person.communities.add(subcommunity.get())
                            logger.debug("Community '" + community_name +
                                         "' added.")
                        else:
                            logger.debug("'" + community_name + "' not found.")
            else:
                logger.error("User has handle but LDAP can't find him/her!")
            logger.debug("Created new person '" + person.handle + "'")
            person.save()
        else:
            person = person_set.get()

        # Create new user if not already available
        if not person.user:
            try:
                user = User.objects.get(username=person.handle)
            except:
                user = User()
                user.username = person.handle
                user.first_name = person.name.split()[0]
                user.is_staff = True
                user.email = email
                user.set_password(utils.id_generator(size=12))
                user.save()
            person.user = user
            person.save()
            logger.debug("User '{}' linked to person '{}'".
                         format(user, person))
        user = person.user
        user = authenticate(username=user.username)
        login(request, user)
        logger.debug("Logged in user '{}'".format(user))
    else:
        logger.debug("Authentication failed")
    return HttpResponseRedirect('/')


def cast_vote(request):
    # TODO explicitly define upvotes and downvotes
    # TODO something about not upvoting your own comments
    if request.method == "POST" and request.is_ajax():
        model_type = request.POST.get("model", None)
        model_id = request.POST.get("id", None)
        vote = request.POST.get("vote", None)
        if model_type is None or model_id is None or vote is None:
            return HttpResponseBadRequest()

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
                    return HttpResponse('You can only vote once.', status=403)
            else:
                if not model.downvoters.filter(pk=user.pk).exists():
                    if model.upvoters.filter(pk=user.pk).exists():
                        model.upvoters.remove(user)
                    else:
                        model.downvoters.add(user)
                else:
                    return HttpResponse('You can only vote once.', status=403)
            model.save()
            return HttpResponse()
        else:
            return HttpResponse('You need to login first.', status=401)
    else:
        return HttpResponseBadRequest()


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
            try:
                request.POST._mutable = True
                request.POST['author'] = request.user.person
                request.POST._mutable = False
            except Person.DoesNotExist:
                # TODO Present message to the user explaining that somehow
                # he is not linked to a person object.
                return HttpResponseNotFound()
            finally:
                request.POST._mutable = False
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
                    # TODO Present message to the user explaining that somehow
                    # he is not linked to a person object.
                    return HttpResponseNotFound()

                logger.debug("Question submitted by user '{}'".format(
                    request.user))
                question.save()
                questionform.save_m2m()

                # Create reflexive links
                if item:
                    item.link(question)
                    question.link(item)

                # Assign communities
                c1 = set(item.communities.all())
                c2 = set(question.author.communities.all())
                for community in c1.intersection(c2):
                    question.communities.add(community)

                data = json.dumps({'success': True,
                                   'redirect': question.get_absolute_url()})

                # Send email
                text_content = question.text
                html_content = ("<h3><a href='http://" + HOSTNAME +
                                question.get_absolute_url() + "'>" +
                                question.title + "</a></h3><p><i>by " +
                                question.author.name + "</i></p>" +
                                question.text)
                subject = "Starfish question: " + question.title
                from_email = "notifications@" + HOSTNAME
                to = ADMIN_NOTIFICATION_EMAIL
                msg = EmailMultiAlternatives(subject, text_content, from_email,
                                             to)
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)
            else:
                logger.debug("questionform invalid")
                r = {'success': False,
                     'errors': dict([(k, [unicode(e) for e in v])
                                     for k, v in questionform.errors.items()])}
                data = json.dumps(r)
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
            return HttpResponseBadRequest("Input was not valid")
    else:
        return HttpResponseBadRequest("This HTTP method is not supported.")


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
        return redirect('/?q=' + symb + handle)
    if tag.glossary is not None:
        return redirect(tag.glossary.get_absolute_url())
    elif tag.alias_of is not None and tag.alias_of.glossary is not None:
        return redirect(tag.alias_of.glossary.get_absolute_url())
    else:
        return redirect('/?q=' + symb + handle)


def browse(request):
    user_communities = utils.get_user_communities(request.user)
    selected_community = request.GET.get("community", None)
    if selected_community is not None:
        try:
            selected_community = Community.objects.get(
                    pk=int(selected_community))
        except Community.DoesNotExist:
            selected_communities = user_communities
        else:
            selected_communities = [selected_community]
        # Filter check disabled, to allow anyone with access to link to view
        # selected_communities = filter(lambda x: x.id == selected_community,
        #        user_communities)
        selected_communities = utils.expand_communities(selected_communities)
    else:
        selected_communities = user_communities
    items = Item.objects.filter(communities__in=selected_communities)

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
        'user_communities': user_communities,
        'results': results_by_type,
        'cols': 1,
        'first_active': first_active,
    })


def search(request):
    user_communities = utils.get_user_communities(request.user)
    string = request.GET.get('q', '')
    community = request.GET.get('community', '')
    if len(string) > 0:
        # Check if community selected, if so, use it
        if community.isdigit() and int(community) > 0:
            community = int(community)
            try:
                search_communities = [Community.objects.get(pk=int(community))]
            except Community.DoesNotExist:
                search_communities = user_communities
        else:
            search_communities = user_communities
        query, dym_query, dym_query_raw, results, special = \
                retrieval.retrieve(string, True, search_communities)

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
        used_tags_by_type = []
    else:
        query = ""
        dym_query = query
        dym_query_raw = query
        results_by_type = {}
        special = None
        first_active = ""
        used_tags = set([x.tag for x in
            Item.tags.through.objects.all() if
                len(set(user_communities)&set(x.item.communities.all()))])
        used_tags_by_type = []
        for tag_type in Tag.TAG_TYPES:
            tags = [tag.handle for tag in used_tags if
                tag.type == tag_type[0]]
            random.shuffle(tags)
            used_tags_by_type.append([
                tag_type,
                sorted(tags[0:10])
            ])

    # do not return events that are past due date
    #if 'Event' in results_by_type:
    #    results_by_type['Event'] = [e for e in results_by_type['Event']
    #                                if not e['is_past_due']]

    return render(request, 'index.html', {
        'special': special,
        'results': results_by_type,
        'syntax': SEARCH_SETTINGS['syntax'],
        'query': query,
        'dym_query': dym_query,
        'dym_query_raw': dym_query_raw,
        'cols': 1,      # replaces len(results_by_type)
        'first_active': first_active,
        'user_communities': user_communities,
        'community': community,
        'used_tags': used_tags_by_type,
    })

def feedback(request):
    user_communities = utils.get_user_communities(request.user)
    return render(request, 'feedback.html', {
        "user_communities": user_communities})

def search_list(request):
    user_communities = utils.get_user_communities(request.user)
    string = request.GET.get('q', '')
    if len(string) > 0:
        query, dym_query, dym_query_raw, results, special = \
                retrieval.retrieve(string, True, user_communities)

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
                   'dym_query_raw': dym_query_raw,
                   'user_communities': user_communities,
                   })

def get_model_by_sub_id(model_type, model_id):
    ''' We know the model_id and type, but the id
    identifies it among its equals.. and not all models!
    '''
    # TODO replace using downcast
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
