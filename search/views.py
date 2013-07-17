from django.shortcuts import render, get_object_or_404
from django.views import generic

from search.models import Info


class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'latest_info_list'

    def get_queryset(self):
        return Info.objects.order_by('-pub_date')[:10]

class InfoView(generic.DetailView):
    template_name = 'search/info.html'
    model = Info
