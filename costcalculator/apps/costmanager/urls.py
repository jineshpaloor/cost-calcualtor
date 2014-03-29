from django.conf.urls import patterns, url #, include
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from costcalculator.apps.costmanager import views


urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(views.BillingHomeView.as_view()), name='billing-home'),
    url(r'^add_bill/$', views.BillCreateView.as_view(), name='create-bill'),
    url(r'^generate_bill/$', views.MonthlyBillCreateView.as_view(), name='generate-monthly-bill'),

)
