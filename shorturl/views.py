from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render

from .forms import URLForm
from .models import URL


def index(request):
    if request.method == 'POST':
        url_form = URLForm(request.POST)
        if url_form.is_valid():
            url_obj = URL.get_or_create_short_url(
                long_url=url_form.cleaned_data['long_url'])
            return render(
                request,
                'shorturl/success.html', {'url_obj': url_obj}
            )
    else:
        url_form = URLForm()
    return render(request, 'shorturl/index.html', {'url_form': url_form})


def short_url(request, short_url_path_component):
    url_obj = URL.objects.filter(
        converted_url__combination=short_url_path_component).first()
    if not url_obj:
        return HttpResponse('Invalid short URL!')

    url_obj.visit_count += 1
    url_obj.save()

    return HttpResponseRedirect(url_obj.long_url)


def url_detail(request, short_url_path_component):
    url_obj = URL.objects.filter(
        converted_url__combination=short_url_path_component).first()
    if not url_obj:
        return HttpResponse('Invalid short URL!')

    return render(
        request,
        'shorturl/details.html',
        {'url_obj': url_obj},
    )
