import datetime

from django.shortcuts import render_to_response
#from django.http import HttpResponse
from django.db.models import Sum
from django.template import RequestContext
from django.views import generic

# Create your views here.
from costcalculator.apps.costmanager.models import Bill


def home(request):
    d = datetime.date.today()
    year, month = d.year, d.month
    bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
    group_wise_bills = bills.values('group__name').annotate(tot_amt=Sum('amount'))
    user_wise_bills = bills.values('spend_by__username').annotate(tot_amt=Sum('amount'))
    return render_to_response('costmanager/bill_home.html',
            {'group_wise_bills':group_wise_bills, 'user_wise_bills':user_wise_bills, 'year':year, 'month':month},
            context_instance=RequestContext(request))

class BillListView(generic.ListView):
    template_name = 'costmanager/bill_list.html'

    def get_queryset(self):
        d = datetime.date.today()
        year, month = d.year, d.month
        return Bill.objects.filter(spend_on__year=year, spend_on__month=month)
