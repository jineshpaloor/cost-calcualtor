from django.contrib import admin
from django.contrib.auth.models import User
from costcalculator.apps.costmanager.models import PersonalInfo,Group, \
        Category, SubCategory, Bill

# Register your models here.
admin.site.register(PersonalInfo)

class UserInline(admin.StackedInline):
    model = User
    extra = 3

class GroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Description', {'fields': ['description']}),
        ('Members', {'fields': ['members'],
                              'classes': ['collapse']}),
    ]
    #inlines = [UserInline]

admin.site.register(Group, GroupAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Bill)
