from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from models import Gmina, Obwod

def index(request):
    gminy_list = Gmina.objects.all()
    output = ", ".join([g.nazwa for g in gminy_list])
    template = loader.get_template('obwody/index.html')
    context = RequestContext(request, {
        'gminy_list': gminy_list,
        })
    return HttpResponse(template.render(context))

def detail(request, gmina_id):
    return HttpResponse("Odpaliles gmine %s." % gmina_id)

def results(request, gmina_id):
    response = "Obczajasz gmine %s."
    return HttpResponse(response % gmina_id)

def vote(request, gmina_id):
    return HttpResponse("Updatujesz %s." % gmina_id)
