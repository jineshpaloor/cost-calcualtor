from django.forms import ModelForm

from costcalculator.apps.costmanager.models import Bill

class BillForm(ModelForm):

    class Meta:
        model = Bill
