import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect#, HttpResponse
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.views.generic import ListView

# Create your views here.
from costcalculator.apps.costmanager.models import Bill, MonthlyUserBill


class HomePageView(TemplateView):

    template_name = 'costmanager/landing_page.html'


class BillListView(ListView):

    template_name = 'costmanager/bill_list.html'

    def get_queryset(self):
        d = datetime.date.today()
        year, month = d.year, d.month
        return Bill.objects.filter(spend_on__year=year, spend_on__month=month)


def bill_summary(request):
    d = datetime.date.today()
    month_str = d.strftime('%B')
    year, month = d.year, d.month
    bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
    group_wise_bills = bills.values('group__name').annotate(tot_amt=Sum('amount'))
    user_wise_bills = bills.values('spend_by__username').annotate(tot_amt=Sum('amount'))
    gross_total = bills.aggregate(amt=Sum('amount'))['amt']
    user_bills = MonthlyUserBill.objects.all()
    return render_to_response('costmanager/bill_home.html',
            {'group_wise_bills':group_wise_bills,
             'user_wise_bills':user_wise_bills, 'year':year,
             'month':month_str, 'gross_total':gross_total,
             'user_bills':user_bills},
            context_instance=RequestContext(request))


def generate_monthly_bill(request):
    users = User.objects.all()
    year = request.POST.get('year')
    month = request.POST.get('month')
    for user in users:
        MonthlyUserBill.objects.generate_bill(user, year, month)
    return HttpResponseRedirect(reverse('billing-home'))


def group_wise_bills(request):
    d = datetime.date.today()
    year, month = d.year, d.month
    bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
    group_wise_bills = bills.values('group__name').annotate(tot_amt=Sum('amount'))
    return render_to_response('costmanager/group_wise_bill.html',
            {'group_wise_bills':group_wise_bills},
            context_instance=RequestContext(request))


def user_wise_bills(request):
    d = datetime.date.today()
    year, month = d.year, d.month
    bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
    user_wise_bills = bills.values('spend_by__username').annotate(tot_amt=Sum('amount'))
    return render_to_response('costmanager/user_wise_bill.html',
            {'user_wise_bills':user_wise_bills},
            context_instance=RequestContext(request))


def monthly_bill(request):
    d = datetime.date.today()
    year, month = d.year, d.month
    bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
    gross_total = bills.aggregate(amt=Sum('amount'))['amt']
    user_bills = MonthlyUserBill.objects.all()
    return render_to_response('costmanager/monthly_bill.html',
            {'gross_total':gross_total, 'user_bills':user_bills},
            context_instance=RequestContext(request))
