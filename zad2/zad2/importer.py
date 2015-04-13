from itertools import izip
from obwody.models import Gmina, Obwod
from django.utils import timezone

def pairwise(t):
    it = iter(t)
    return izip(it,it)

lines = [line.strip() for line in open('dane_old')]

for pair in pairwise(lines):
    try:
        gmina = Gmina.objects.get(nazwa=pair[1])
    except:
        gmina = Gmina(nazwa=pair[1], aktualizacja=timezone.now())
        gmina.save()

    try:
        obwod = Obwod.objects.get(nazwa=pair[0])
    except:
        obwod = Obwod(nazwa=pair[0], gmina=gmina)
        obwod.save()
        print Obwod.objects.count()
