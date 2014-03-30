import datetime

from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, CreateView #, DetailView
from django.views.generic.base import TemplateView

# Create your views here.
from costcalculator.apps.costmanager.models import Bill, MonthlyUserBill
from costcalculator.apps.costmanager.forms import MonthlyBillingForm, BillForm


class HomePageView(TemplateView):

    template_name = 'costmanager/landing_page.html'


class BillingHomeView(ListView):

    context_object_name = 'bill_list'
    model = Bill
    template_name = 'costmanager/bill_home.html'

    def get_queryset(self):
        d = datetime.date.today()
        year, month = d.year, d.month
        return Bill.objects.filter(spend_on__year=year, spend_on__month=month)

    def get_context_data(self, **kwargs):
        # call super class method
        context = super(BillingHomeView, self).get_context_data(**kwargs)

        d = datetime.date.today()
        year, month = d.year, d.month
        context['year'] = year
        context['month'] = month
        context['month_str'] = d.strftime('%B')

        bills = Bill.objects.filter(spend_on__year=year, spend_on__month=month)
        context['bills'] = bills
        context['group_wise_bills'] = bills.values('group__name').annotate(tot_amt=Sum('amount'))
        context['user_wise_bills'] = bills.values('spend_by__username').annotate(tot_amt=Sum('amount'))
        context['gross_total'] = bills.aggregate(amt=Sum('amount'))['amt']
        context['user_bills'] = MonthlyUserBill.objects.all()
        context['bill_form'] = BillForm()
        context['monthly_bill_form'] = MonthlyBillingForm()
        return context


class BillListView(ListView):

    model = Bill
    template_name = 'costmanager/bill_list.html'

    def get_queryset(self):
        d = datetime.date.today()
        year, month = d.year, d.month
        return Bill.objects.filter(spend_on__year=year, spend_on__month=month)

class BillCreateView(CreateView):

    form_class = BillForm
    success_url = reverse_lazy('billing-home')


class MonthlyBillCreateView(CreateView):

    form_class = MonthlyBillingForm
    success_url = reverse_lazy('billing-home')


def generate_monthly_bill(request):
    users = User.objects.all()
    billing_from = request.POST.get('billing_from')
    billing_to = request.POST.get('billing_to')
    for user in users:
        MonthlyUserBill.objects.generate_bill(user, billing_from, billing_to)
    return HttpResponseRedirect(reverse('billing-home'))

