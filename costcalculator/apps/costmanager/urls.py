from django.conf.urls import patterns, url #, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from costcalculator.apps.costmanager import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.BillListView.as_view(), name='bill-home'),
    url(r'^generate_bill/$', views.generate_bill, name='generate-bill'),

)
