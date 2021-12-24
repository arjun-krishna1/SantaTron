from django.urls import path

from .views import createPoolView

urlpatterns = [
    path('create/', createPoolView, name="createPoolUrl"),
]
