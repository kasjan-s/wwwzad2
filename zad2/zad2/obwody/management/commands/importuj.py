from itertools import izip
from obwody.models import Gmina, Obwod
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Importuje gmine i obwody z list'

    def handle(self, *args, **options):
        def pairwise(t):
            it = iter(t)
            return izip(it,it)

        lines = [line.strip() for line in open('dane')]
        counter = 0
        for pair in pairwise(lines):
            counter += 1
            if counter % 100 is 0:
                print counter
            try:
                gmina = Gmina.objects.get(nazwa=pair[1])
            except:
                gmina = Gmina(nazwa=pair[1])
                gmina.save()

            try:
                obwod = Obwod.objects.get(nazwa=pair[0])
            except:
                obwod = Obwod(nazwa=pair[0], gmina=gmina, aktualizacja=timezone.now())
                obwod.save()
