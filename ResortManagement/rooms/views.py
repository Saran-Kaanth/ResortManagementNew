from queue import Empty
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import rooms
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView
from .models import Rooms
from datetime import datetime
from django.db import connection
# from django.http import request
# Create your views here.



# @staff_member_required
class RoomsCreationView(FormView):
    form_class=RoomsCreationForm
    success_url=reverse_lazy('staffhome')
    template_name='users/room_creation.html'


    def form_valid(self, form) :
        form.save()
        message="Data Saved Successfully"
        form=self.form_class
        return render(self.request,"users/room_creation.html",locals())

    def form_invalid(self, form):
        error_message="Check with your data"
        form=self.form_class
        return render(self.request,"users/room_creation.html",locals())
        
        # return super().form_valid(form)
    # def post(self,request,*args,**kwargs):
    #     print(request.POST)
    #     return super().post(request,*args,**kwargs)

class RoomsListView(ListView):
    model=Rooms
    template_name="users/roomslist.html"
    context_object_name="rooms_list"

    # def get_queryset(self) :
    #     print("hii")
    #     rooms_list=Rooms.objects.raw("select * from rooms_Rooms limit 2")
    #     # print(rooms_list)
    #     for room in Rooms.objects.raw("select * from rooms_Rooms"):
    #         print(room)
    #     return rooms_list

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        print(not self.request.GET)
        context=super().get_context_data(**kwargs)
        context['form']=RoomsSearchFrom()
        # context['rooms_list']=Rooms.objects.raw("select * from rooms_Rooms  where room_type='Classic' and room_no='C324'")
        if not self.request.GET:
            context['name']='saran'
        print(context)
        self.request.session['testname']='testing'
        return context

class RoomDetailView(DetailView):
    model= Rooms
    template_name="users/roomdetail.html"
    # name=request.session['testname']

    # def get_object(self, queryset):
    #     print(queryset)
    #     return super().get_object(queryset)

    def get_context_data(self, **kwargs) :
        print("hi")
        context=super().get_context_data(**kwargs)
        context['testname']=self.request.session['testname']
        return context
        # return super().get_context_data(**kwargs)

    # def get(self, request, *args, **kwargs):
    #     print(self.request.session['testname'])
    #     testname=self.request.session['testname']
    #     return super().get(request, *args, **kwargs)


    # def get(self, request, *args, **kwargs) :
    #     print(request.GET)
    #     if request.GET.get('email') is None:
    #         return super().get(request, *args, **kwargs)
    #         # return render(self.request,"users/roomslist.html",locals())     
    #     else:    
    #         return render(self.request,"users/roomslist.html",locals())


class SampleView(FormView):
    form_class=SampleForm
    template_name: str='users/sample.html'

    def get(self, request,*args,**kwargs):
        check_in_date="04/23/23"
        check_out_date="04/24/23"

        check_in = datetime.strptime(check_in_date, '%m/%d/%y').date()
        check_out = datetime.strptime(check_out_date, '%m/%d/%y').date()


        # cursor=connection.cursor()
        # cur_data=cursor.execute("select * from rooms_Reservation").fetchall()
        # print(cur_data)
        sample=Reservation.objects.all()


        for samp in sample:
            print(check_in,">=",samp.booked_from,"=",check_in>=samp.booked_from)
            print(check_out,"<=",samp.booked_till,check_out<=samp.booked_till)
        data=Reservation.objects.raw('''Select id,booked_room_id from rooms_reservation as reservation
                                    ''')
        # data=Reservation.objects.filter(booked_from__gte=check_in,booked_till__lte=check_out)
        print(data.query)
        for room in data:
            print(room)

        return render(self.request,"users/sample.html",locals())
