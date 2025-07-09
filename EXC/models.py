from django.db import models
from django.contrib.auth.models import User

class userWallet(models.Model):
    addr = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USDT_balance = models.IntegerField(default=0)
    ETH_balance = models.IntegerField(default=0)
    XPR_balance = models.IntegerField(default=0)
    SOL_balance = models.IntegerField(default=0)
    BTC_balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class price(models.Model):
    BTC = models.IntegerField(default=107754)
    ETH = models.IntegerField(default=2485)
    USDT = models.IntegerField(default=1.0002)
    XPR = models.IntegerField(default=2.1885)
    SOL = models.IntegerField(default=150)
