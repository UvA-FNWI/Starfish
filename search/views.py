from django.shortcuts import render, get_object_or_404

from search.models import Info


def index(request):
    latest_info_list = Info.objects.order_by('-date')[:10]
    context = {'latest_info_list': latest_info_list}
    return render(request, 'search/index.html', context)

def info(request, info_id):
    info = get_object_or_404(Info, pk=info_id)
    context = {'info': info}
    return render(request, 'search/info.html', context)
