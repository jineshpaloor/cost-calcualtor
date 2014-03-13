import calendar

from django.db import models

class PersonalInfo(models.Model):
    user = models.OneToOneField('auth.User')
    mobile = models.CharField(max_length=15, blank=True)
    company = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return '{0}'.format(self.user.username)

class Group(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField('auth.User')
    description = models.TextField(max_length=100)

    def __unicode__(self):
        return '{0}'.format(self.name)

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)

    def __unicode__(self):
        return '{0}'.format(self.name)

class SubCategory(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return '{0}'.format(self.name)

class Bill(models.Model):
    category = models.ForeignKey(SubCategory)
    spend_by = models.ForeignKey('auth.User')
    group = models.ForeignKey(Group)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    spend_on = models.DateTimeField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return '{0} - {1} - {2} - {3} - {4}'.format(self.spend_by.username, self.amount, self.category, self.added_on.date(), self.comment)

class UserBillManager(models.Manager):

    def generate_bill(self, user, year, month):
        groups = Group.objects.filter(members=user)
        total_amount = 0
        # calculate user cost per group and add it to total_amount variable
        for group in groups:
            bills = Bill.objects.filter(group=group, spend_on__year=year, spend_on__month=month).aggregate(total=models.Sum('amount'))
            group_strength = group.members.only('id').count()
            total_cost = bills.get('total') if bills.get('total') else 0
            per_head_cost = total_cost / group_strength
            total_amount += per_head_cost

        start_date, end_date = calendar.monthrange(year, month)
        billing_date = '{0}-{1}-{2}'.format(year, month, end_date)
        monthly_bill, created = MonthlyUserBill.objects.get_or_create(user=user, billing_date=billing_date)
        spend_bills = Bill.objects.filter(spend_by=user, spend_on__year=year, spend_on__month=month).aggregate(total=models.Sum('amount'))
        amount_spend = spend_bills.get('total') if spend_bills.get('total') else 0
        monthly_bill.total_amount = total_amount
        monthly_bill.amount_spend = amount_spend
        monthly_bill.amount_to_pay = total_amount - amount_spend
        monthly_bill.save()
        return monthly_bill

class MonthlyUserBill(models.Model):
    user = models.ForeignKey('auth.User')
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.0, null=True, blank=True)
    amount_spend = models.DecimalField(max_digits=7, decimal_places=2, default=0.0, null=True, blank=True)
    amount_to_pay = models.DecimalField(max_digits=7, decimal_places=2, default=0.0, null=True, blank=True)
    billing_date = models.DateTimeField()

    objects = UserBillManager()
