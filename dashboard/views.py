from django.core.context_processors import csrf
from django.shortcuts import render, get_object_or_404, redirect, \
    render_to_response
from django.forms.models import modelform_factory
from django.views import generic
from django.http import HttpResponse
from search.models import *
from steep.settings import SEARCH_SETTINGS
from redactor.widgets import RedactorEditor
from search.forms import *


def contribute(request):
    return render(request, 'contribute_options.html')


def contributions(request):
    if request.user.is_authenticated():
        person = Person.objects.get(user=request.user)
        person = Person.objects.get(pk=1)
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
        if len(elems) == 3:
            obj_id = int(elems[2])
            obj = get_object_or_404(self.model_class, pk=obj_id)
            form = self.form_class(instance=obj)
            c = {"form": form}
        else:
            c = {"form": self.form_class}

        c.update(csrf(request))
        return render_to_response(self.template_name, c)

    def put(self, request, *args, **kwargs):
        """Update an existing Object."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseBadRequest(form.errors)

    def post(self, request, *args, **kwargs):
        """Post a new Object."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseBadRequest(form.errors)


class InformationForm(EditForm):
    template_name = "information_form.html"
    form_class = EditInformationForm
    model_class = Information


class GoodPracticeForm(EditForm):
    template_name = "goodpractice_form.html"
    form_class = EditGoodPracticeForm
    model_class = GoodPractice


class EventForm(EditForm):
    template_name = "event_form.html"
    form_class = EditEventForm
    model_class = Event


class ProjectForm(EditForm):
    template_name = "project_form.html"
    form_class = EditProjectForm
    model_class = Project


class QuestionForm(EditForm):
    template_name = "question_form.html"
    form_class = QuestionForm
    model_class = Question


class GlossaryForm(EditForm):
    template_name = "glossary_form.html"
    form_class = EditGlossaryForm
    model_class = Glossary
