from django.forms import ModelForm
from models import Obwod

import datetime

class ObwodForm(ModelForm):
    class Meta:
        model = Obwod
        exclude = ['gmina', 'nazwa']
