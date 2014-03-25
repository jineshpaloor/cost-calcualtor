import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect#, HttpResponse
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.views import generic

# Create your views here.
from costcalculator.apps.costmanager.models import Bill, MonthlyUserBill


def home(request):
    return render_to_response('costmanager/landing_page.html',
            {}, context_instance=RequestContext(request))

class HomePageView(TemplateView):

    template_name = 'costmanager/landing_page.html'


def bill_summary(request):
    d = datetime.date.today()
    year, month = d.year, d.month
    bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
    group_wise_bills = bills.values('group__name').annotate(tot_amt=Sum('amount'))
    user_wise_bills = bills.values('spend_by__username').annotate(tot_amt=Sum('amount'))
    gross_total = bills.aggregate(amt=Sum('amount'))['amt']
    user_bills = MonthlyUserBill.objects.all()
    return render_to_response('costmanager/bill_home.html',
            {'group_wise_bills':group_wise_bills,
             'user_wise_bills':user_wise_bills, 'year':year,
             'month':month, 'gross_total':gross_total,
             'user_bills':user_bills},
            context_instance=RequestContext(request))


class BillListView(generic.ListView):
    template_name = 'costmanager/bill_list.html'

    def get_queryset(self):
        d = datetime.date.today()
        year, month = d.year, d.month
        return Bill.objects.filter(spend_on__year=year, spend_on__month=month)

def generate_bill(request):
    users = User.objects.all()
    year = 2014
    month = 02
    for user in users:
        MonthlyUserBill.objects.generate_bill(user, year, month)
    return HttpResponseRedirect(reverse('billing-home'))
