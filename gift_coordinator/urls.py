from django.urls import path

from .views import (
    createPoolView,
    listPoolView,
)

urlpatterns = [
    path('', listPoolView, name="listPoolUrl"),
    path('create/', createPoolView, name="createPoolUrl"),
]
