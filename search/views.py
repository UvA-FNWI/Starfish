from django.shortcuts import render

from search.models import Info


def index(request):
    latest_info_list = Info.objects.order_by('-date')[:10]
    context = {'latest_info_list': latest_info_list}
    return render(request, 'search/index.html', context)
