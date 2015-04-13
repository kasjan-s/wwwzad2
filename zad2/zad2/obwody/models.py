from django.db import models

class Gmina(models.Model):
    nazwa = models.CharField(max_length=200)
    aktualizacja = models.DateTimeField('Ostatnia aktualizacja')

    def __unicode__(self):
        return self.nazwa

class Obwod(models.Model):
    nazwa = models.CharField(max_length=300)
    gmina = models.ForeignKey(Gmina)
    karty = models.IntegerField(default=0)
    wyborcy = models.IntegerField(default=0)

    def __unicode__(self):
        return self.nazwa
