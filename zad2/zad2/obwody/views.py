from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.forms.models import modelformset_factory
from models import Gmina, Obwod
from forms import ObwodForm

import datetime
import time
import pytz
import json


def index(request):
    gminy_list = Gmina.objects.all().order_by('nazwa')
    output = ", ".join([g.nazwa for g in gminy_list])
    template = loader.get_template('obwody/index.html')
    context = RequestContext(request, {
        'gminy_list': gminy_list,
        })
    return HttpResponse(template.render(context))

def detail(request, gmina_id):
    gmina = get_object_or_404(Gmina, pk=gmina_id)
    obwody = gmina.obwod_set.all()
    return render(request, 'obwody/detail.html', {'gmina': gmina, 'obwody': obwody})

def obwod(request, obwod_id):
    obwod = Obwod.objects.get(pk=obwod_id)
    if request.method == 'POST':
        karty = request.POST.get('karty')
        wyborcy = request.POST.get('wyborcy')
        czas = datetime.datetime.fromtimestamp(float(request.POST.get('czas')))
        czas_aware = pytz.utc.localize(czas)

        if czas_aware > obwod.aktualizacja:
            obwod.karty = karty
            obwod.wyborcy = wyborcy
            obwod.aktualizacja = czas_aware
            obwod.save()

            response_data = {}
            response_data['result'] = 1
            response_data['result_msg'] = 'Sukces!'
            response_data['karty'] = obwod.karty
            response_data['wyborcy'] = obwod.wyborcy
        else:
            response_data = {}
            response_data['result'] = 0
            response_data['result_msg'] = 'Ktos zmodyfikowal pola w miedzyczasie!'
            response_data['karty'] = obwod.karty
            response_data['wyborcy'] = obwod.wyborcy


        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'karty': obwod.karty, 'wyborcy': obwod.wyborcy}), content_type="application/json")

def results(request, gmina_id):
    response = "Obczajasz gmine %s."
    return HttpResponse(response % gmina_id)

def vote(request, gmina_id):
    return HttpResponse("Updatujesz %s." % gmina_id)
