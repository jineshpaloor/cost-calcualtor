from django.forms import ModelForm
from django.contrib.auth.models import User

from costcalculator.apps.costmanager.models import Bill, MonthlyUserBill

class BillForm(ModelForm):

    class Meta:
        model = Bill


class MonthlyBillingForm(ModelForm):

    class Meta:
        model = MonthlyUserBill
        fields = ['billing_from', 'billing_to']

    def save(self, commit=True):
        instance = super(MonthlyBillingForm, self).save(commit=False)

        if commit:
            users = User.objects.all()
            billing_from = self.cleaned_data.get('billing_from')
            billing_to = self.cleaned_data.get('billing_to')
            for user in users:
                MonthlyUserBill.objects.generate_bill(user, billing_from, billing_to)

        return instance
