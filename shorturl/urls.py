from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?:!(.*))$',
        views.url_detail, name='url_detail'),
    url(r'^(?P<short_url_path_component>[0-9a-zA-z]+)$',
        views.short_url, name='short_url'),

]