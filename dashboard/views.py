from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import modelform_factory
from search.models import Person
from steep.settings import SEARCH_SETTINGS
from redactor.widgets import RedactorEditor

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
