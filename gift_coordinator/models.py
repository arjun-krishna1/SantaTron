from django.db import models
from django.utils import timezone


class GiftPool(models.Model):
    recipient_name = models.CharField(max_length=100, default="")
    creation_date = models.DateTimeField('date created', default=timezone.now)
    curr_val = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    search_query = models.CharField(max_length=200, default='')
    url = models.CharField(max_length=300, default='')


class Contributor(models.Model):
    name = models.CharField(max_length=100, default="")
    amount_contributed = models.DecimalField(decimal_places=2, max_digits=8, default = 0)
    gift_pool = models.ForeignKey(GiftPool, on_delete=models.CASCADE)
    keyword1 = models.CharField(max_length=50, default="")
    keyword2 = models.CharField(max_length=50, default="")
    keyword3 = models.CharField(max_length=50, default = "")

# source query by filtering all contributor objects linked to pool, extracting keyword fields, and passing to model/API
# for debug purposes, construct search query on each new contributor
