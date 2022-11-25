from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# create your models here

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    balance = models.CharField(max_length=100, null=True, default=0)
    phone_no = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    user_type = models.IntegerField(null=True, default=0)
    verification_code = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)

    def __str__(self):
         return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# create kyc model
class bank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    routing_no = models.CharField(max_length=30, default='')
    bank_name = models.CharField(max_length=100, default='')
    account_no = models.CharField(max_length=30, default='')
    account_name = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name+' '+ self.user.last_name
    

    class Meta():
        db_table = 'bank'

@receiver(post_save, sender=User)
def create_bank(sender, instance, created, **kwargs):
    if created:
        bank.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_bank(sender, instance, **kwargs):
    instance.bank.save()


# creat deposit here
class deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trx_id = models.CharField(max_length=500, null=True, unique=True)
    reference_id = models.CharField(max_length=500, null=True, unique=True)
    amount = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.trx_id
    

    class Meta():
        db_table = 'deposit'

class withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trx_id = models.CharField(max_length=500, null=True, unique=True)
    amount = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.trx_id

    class Meta():
        db_table = 'withdraw'

# creat model for pla
class trading_plan(models.Model):
    name = models.CharField(max_length=100, null=True)
    plan_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    minimum = models.CharField(max_length=100, null=True)
    maximum = models.CharField(max_length=100, null=True)
    daily_profit = models.CharField(max_length=100, null=True)
    duration = models.CharField(max_length=100, null=True)
    withdraw_type = models.CharField(max_length=100, null=True)
    ref = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'trading_plan'


# creat investment model 
class tradings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trading_plan = models.ForeignKey(trading_plan, on_delete=models.CASCADE, null=True)
    amount = models.CharField(max_length=100, null=True)
    daily_profit = models.CharField(max_length=100, null=True)
    net_profit = models.CharField(max_length=100, null=True)
    duration = models.IntegerField(max_length=100, null=True)
    active_days = models.IntegerField(null=True)
    next_day = models.DateTimeField(max_length=100, null=True)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(max_length=100, null=True)
    withdraw_type = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True)

    def __str__(self):
        return self.trading_plan.name 

    class Meta():
        db_table = 'tradings'


# create teh earnings structure
class earnings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tradings = models.ForeignKey(tradings, on_delete=models.CASCADE, null=True)
    amount = models.CharField(max_length=30, null=True)
    date = models.DateTimeField()
    def __str__(self):
        return self.user.username

    class Meta():
        db_table = 'earnings'