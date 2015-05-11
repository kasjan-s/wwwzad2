from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.forms.models import modelformset_factory
from models import Gmina, Obwod
from forms import ObwodForm

import datetime
import time
import pytz


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
    if request.method == 'POST':
        wersja = datetime.datetime.fromtimestamp(float(request.POST['czas_odczytu']))
        wersja = pytz.utc.localize(wersja)
        ObwodFormSet = modelformset_factory(Obwod, exclude=['gmina', 'nazwa', 'aktualizacja'])
        formset = ObwodFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            fail_msgs = []
            for instance in instances:
                if instance.aktualizacja <= wersja:
                    instance.aktualizacja = wersja
                    instance.save()
                else:
                    obwod = Obwod.objects.get(pk=instance.pk)
                    roznica = (pytz.utc.localize(datetime.datetime.now()) - instance.aktualizacja).total_seconds()
                    fail_msg = "Ktos cos zmienil dla obwod %s %d sekund temu! Wpisujesz %d i %d, a jest %d i %d" % (instance.nazwa, roznica,instance.karty, instance.wyborcy, obwod.karty, obwod.wyborcy)
                    fail_msgs.append(fail_msg)


            if fail_msgs:
                for form in formset:
                    form.moja_nazwa = form.instance.nazwa
                return render(request, 'obwody/detail.html', {'gmina': gmina, 'formset': formset, 'aktualizacja': time.time(), 'fails': fail_msgs})
            else:
                return redirect('detail', gmina_id=gmina_id)
        else:
            return redirect('detail', gmina_id=gmina_id)
    else:
        ObwodFormSet = modelformset_factory(Obwod, exclude=['gmina', 'nazwa', 'aktualizacja'], extra=0)
        formset = ObwodFormSet(queryset=gmina.obwod_set.all().order_by('nazwa'))
        for form in formset:
            form.moja_nazwa = form.instance.nazwa
        return render(request, 'obwody/detail.html', {'gmina': gmina, 'formset': formset, 'aktualizacja': time.time()})


def results(request, gmina_id):
    response = "Obczajasz gmine %s."
    return HttpResponse(response % gmina_id)

def vote(request, gmina_id):
    return HttpResponse("Updatujesz %s." % gmina_id)
