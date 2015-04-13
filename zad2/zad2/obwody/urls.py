from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<gmina_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<gmina_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<gmina_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
