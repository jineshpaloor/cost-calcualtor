from django.db import models

class PersonalInfo(models.Model):
    user = models.OneToOneField('auth.User')
    mobile = models.IntegerField(blank=True)
    company = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)

class Group(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField('auth.User')
    description = models.TextField(max_length=100)

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)

class SubCategory(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=30)

class Bill(models.Model):
    category = models.ForeignKey(SubCategory)
    spend_by = models.ForeignKey('auth.User')
    group = models.ForeignKey(Group)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=100, null=True, blank=True)
