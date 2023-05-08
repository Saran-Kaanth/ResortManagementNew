from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('createroom/',views.RoomsCreationView.as_view(),name="roomcreate"),
    path('roomslist/',views.RoomsListView.as_view(),name="roomslist"),
    path('<str:pk>/detail/',views.RoomDetailView.as_view(),name="roomdetail"),
]