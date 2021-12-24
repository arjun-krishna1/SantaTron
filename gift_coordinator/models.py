from django.db import models
from django.utils import timezone


class GiftPool(models.Model):
    recip_name = models.CharField(max_length=100)
    creation_date = models.DateTimeField('date created', default = timezone.now())

