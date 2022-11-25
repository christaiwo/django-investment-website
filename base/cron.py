import os
import django
import datetime
from datetime import date
from django.utils import timezone
date = datetime.datetime.today()
current_now = timezone.now()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safedeal.settings')
django.setup()
from base.models import *


def earning():
    active_tradings = tradings.objects.filter(status=1)

    # loop through the trading and reward users 
    for trading in active_tradings:
        if trading.next_day == date :
            if trading.duration == trading.active_days:
                tradings.objects.filter(id=trading.id).update(status=0)
            else:
                user = User.objects.get(id=trading.user_id)
                Profile.objects.filter(user_id=trading.user_id).update(balance=float(user.profile.balance) + float(trading.daily_profit) )

                tradings.objects.filter(id=trading.id).update(active_days=trading.active_days + 1)

                earning_insert = earnings(amount=trading.daily_profit, date=date, tradings_id=trading.id, user_id=trading.user_id)
                earning_insert.save()