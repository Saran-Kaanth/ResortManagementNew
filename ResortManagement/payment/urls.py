from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
        path('paymentreview/',views.PaymentView.as_view(),name='paymentreview'),
        path("callback/", views.callback, name="callback"),
]