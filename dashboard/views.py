from django.core.context_processors import csrf
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import modelform_factory
from django.views import generic
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect
from search.models import *
from django.conf import settings
from redactor.widgets import RedactorEditor
from search.forms import *
from search.utils import parse_tags

SEARCH_SETTINGS = settings.SEARCH_SETTINGS
TAG_REQUEST_MESSAGE = settings.TAG_REQUEST_MESSAGE


def contribute(request):
    return render(request, 'contribute_options.html')


def contributions(request):
    if request.user.is_authenticated():
        person = Person.objects.get(user=request.user)
        c = {}
        c['goodpractice'] = GoodPractice.objects.filter(author=person)
        c['information'] = Information.objects.filter(author=person)
        c['project'] = Project.objects.filter(author=person)
        c['event'] = Event.objects.filter(author=person)
        c['question'] = Question.objects.filter(author=person)
        c['glossary'] = Glossary.objects.filter(author=person)
        return render(request, 'contributions.html', {'c': c})
    else:
        # TODO usability
        return HttpResponse("Please log in.")


def edit_me(request):
    if request.user.is_authenticated():
        person = Person.objects.get(user=request.user)
        PersonForm = modelform_factory(Person)
        if request.method == "POST":
            form = PersonForm(request.POST, instance=person)
            if form.is_valid():
                form.save()
            return render(request, 'dashboard_person.html', {
                'form': form,
                'person': person,
                'syntax': SEARCH_SETTINGS['syntax']})
        else:
            return render(request, 'dashboard_person.html', {
                'form': PersonForm(instance=person),
                'person': person,
                'syntax': SEARCH_SETTINGS['syntax']})
    else:
        # TODO usability
        return HttpResponse("Please log in.")


class EditForm(generic.View):
    success_url = "/dashboard/"

    def get(self, request, *args, **kwargs):
        """Get a form for a new or existing Object."""

        # Existing object
        elems = request.path.strip("/").split("/")
        try:
            obj_id = int(elems[2])
            obj = get_object_or_404(self.model_class, pk=obj_id)
            form = self.form_class(instance=obj)
            c = {"form": form}
        except ValueError:
            c = {"form": self.form_class(
                        {"text": get_template(self.model_class)}),
                 "is_new": True}

        c.update(csrf(request))
        return render(request, self.template_name, c)

    def post(self, request, *args, **kwargs):
        """Post a new object or update existing"""

        # Existing object
        elems = request.path.strip("/").split("/")
        post_v = request.POST.copy()
        post_v["author"] = request.user.person.id
        try:
            obj_id = int(elems[-1])
            obj = get_object_or_404(self.model_class, pk=obj_id)
            form = self.form_class(post_v, instance=obj)
        except ValueError:  # New object
            form = self.form_class(post_v)
        if form.is_valid():
            # Check if all tags are already known
            tag_str = form.data.get('tags', None)
            if tag_str:
                tags, unknown_tags = parse_tags(tag_str)
                if unknown_tags['token'] or unknown_tags['person'] or \
                        unknown_tags['literal']:
                    messages.info(request, TAG_REQUEST_MESSAGE)
            if self.success_url[-1] == '/':
                obj_id = str(form.save().pk)
            else:
                obj_id = '/' + str(form.save().pk)
            redirect = self.success_url + obj_id
            return HttpResponseRedirect(redirect)
        else:
            return render(request, self.template_name, {'form': form})


class InformationForm(EditForm):
    template_name = "information_form.html"
    form_class = EditInformationForm
    model_class = Information
    success_url = "/dashboard/information"


class GoodPracticeForm(EditForm):
    template_name = "goodpractice_form.html"
    form_class = EditGoodPracticeForm
    model_class = GoodPractice
    success_url = "/dashboard/goodpractice"


class EventForm(EditForm):
    template_name = "event_form.html"
    form_class = EditEventForm
    model_class = Event
    success_url = "/dashboard/event"


class ProjectForm(EditForm):
    template_name = "project_form.html"
    form_class = EditProjectForm
    model_class = Project
    success_url = "/dashboard/project"


class QuestionForm(EditForm):
    template_name = "question_form.html"
    form_class = EditQuestionForm
    model_class = Question
    success_url = "/dashboard/question"


class GlossaryForm(EditForm):
    template_name = "glossary_form.html"
    form_class = EditGlossaryForm
    model_class = Glossary
    success_url = "/dashboard/glossary"
