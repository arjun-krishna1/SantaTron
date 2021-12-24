from django.urls import path

from .views import (
    createPoolView,
    listPoolView,
    chooseGiftView
)

urlpatterns = [
    path('', listPoolView, name="listPoolUrl"),
    path('create/', createPoolView, name="createPoolUrl"),
    path('create/<str:recipient_name>/', createPoolView, name="createPoolUrlName"),
    path('choose/<str:recipient_name>/', chooseGiftView, name="chooseGiftUrl"),
]
