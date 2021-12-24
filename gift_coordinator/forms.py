from django.forms import (
    Form,
    CharField,
    IntegerField

)

from .models import GiftPool

# person's name, how much they contribute, 5 key words, submit button
class CreatePoolForm(Form):
    contributor_name = CharField(label='What is your name?', max_length= 100)
    recipient_name = CharField(label='What is the person getting the gift\'s name?', max_length= 100)
    amount = IntegerField(label='How much will you contribute (USD)?')
    keyword1 = CharField(label='A keyword to help me choose a gift', max_length = 10)
    keyword2 = CharField(label='A keyword to help me choose a gift', max_length = 10)
    keyword3 = CharField(label='A keyword to help me choose a gift', max_length = 10)