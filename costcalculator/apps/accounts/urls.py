from django.conf.urls import patterns, url #, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()
# from costcalculator.apps.accounts import views

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page':'/'}, name='logout'),
)
