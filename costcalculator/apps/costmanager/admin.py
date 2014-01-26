from django.contrib import admin
from costcalculator.apps.costmanager.models import PersonalInfo,Group, \
        Category, SubCategory, Bill

# Register your models here.
admin.site.register(PersonalInfo)
admin.site.register(Group)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Bill)
