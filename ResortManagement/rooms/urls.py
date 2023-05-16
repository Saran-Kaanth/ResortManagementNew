from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.views.generic import TemplateView

# app_name = 'rooms'

urlpatterns=[
    path('createroom/',views.RoomsCreationView.as_view(),name="roomcreate"),
    path('roomslist/',views.RoomsListView.as_view(),name="roomslist"),
    path('<str:pk>/detail/',views.RoomDetailView.as_view(),name="roomdetail"),
    path('deletereservation/<int:pk>/confirm',views.ReservationDeleteView.as_view(),name="deletereservation"),
    re_path(r'^checkin/(?P<reservation_id>\w+)/$',views.checkInView,name="checkin"),
    re_path(r'^checkout/(?P<reservation_id>\w+)/$',views.checkOutView,name="checkout"),
    path('thanks/',TemplateView.as_view(template_name="users/thanks.html"),name="thanks"),
    # path('<str:pk>/checkout/',name="checkout"),
]