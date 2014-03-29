from django.conf.urls import patterns, url #, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from costcalculator.apps.reports import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.ReportHomePageView.as_view(), name='reports-home'),
)
