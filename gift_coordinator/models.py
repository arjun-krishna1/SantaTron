from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


class GiftPool(models.Model):
    recip_name = models.CharField(max_length=100)
    creation_date = models.DateTimeField('date created', default=timezone.now())
    curr_val = models.DecimalField(decimal_places=2, max_digits=10)
    search_query = models.CharField(max_length=200)


class Contributor(models.Model):
    name = models.CharField(max_length=100)
    amount_contributed = models.DecimalField(decimal_places=2, max_digits=8)
    gift_pool = models.ForeignKey(GiftPool, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)

# source query by filtering all contributor objects linked to pool, extracting keyword fields, and passing to model/API
# for debug purposes, construct search query on each new contributor
