from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse

from search.models import *


MAX_AUTOCOMPLETE = 5

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_info_list'

    def get_queryset(self):
        return Info.objects.order_by('-pub_date')[:10]


class InfoView(generic.DetailView):
    template_name = 'info.html'
    model = Info


def autocomplete(request):
    try:
        str = request.GET.get('q')
    except:
        return HttpResponse()
    matches = Tag.objects.filter(name__istartswith=str)
    return HttpResponse(matches)

def search(request):
    return render(request, 'search.html')
