from django.conf.urls import patterns, url #, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('costcalculator.apps.costmanager.views',
    # Examples:
    url(r'^$', 'home', name='home'),

)
