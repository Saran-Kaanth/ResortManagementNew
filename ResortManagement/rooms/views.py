from locale import currency
from queue import Empty
from django.shortcuts import render
from django.views.generic.edit import FormView
# from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages
import rooms
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,TemplateView
from .models import Rooms
import datetime as dt
from datetime import datetime, date
import razorpay
# from django.conf import settings
from ResortManagement.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET,EMAIL_HOST_USER
from django.http import HttpResponseBadRequest,HttpResponse
from .constants import *
import json
from django.core.mail import send_mail
# from django.db import connection




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
        

class RoomsListView(ListView):
    model=Rooms
    template_name="users/roomslist.html"
    context_object_name="rooms_list"


    def get_context_data(self, **kwargs):
        check_in=date.today().strftime(("%Y-%m-%d"))
        check_out=(date.today()+dt.timedelta(days=1)).strftime("%Y-%m-%d")
        
        context=super().get_context_data(**kwargs)
        # context['form']=RoomsSearchFrom(data={'check_in':dt.date.today,'check_out':dt.date.today})
        context['form']=RoomsSearchForm(initial={'check_in':check_in,
                                                'check_out':check_out
                                                })
        # print(context['form'].data['check_in'])
        # context['rooms_list']=Rooms.objects.raw("select * from rooms_Rooms  where room_type='Classic' and room_no='C324'")
        if not self.request.GET:
            print("first call")
            print(type(check_in))
            context['rooms_list']=Rooms.objects.raw(f'''
                                                    Select * from rooms_rooms room where room.room_no not in 
                                                    (
                                                        Select reservation.booked_room_id from rooms_reservation reservation, rooms_rooms roomobj
                                                        where reservation.booked_room_id=roomobj.room_no and
                                                        (reservation.booked_from>="{check_in}" and reservation.booked_till<="{check_out}")
                                                    )
                                                    ''')
            self.request.session['check_in']=check_in
            self.request.session['check_out']=check_out
            return context
            
        else:
            #Add condition for checking the dates of room search
            if (self.request.GET['check_in']>=self.request.GET['check_out']):
                print("comparing date")
                context["error_message"]="Check In date should be greater than Check Out date"
                return context

            elif(self.request.GET['check_in']<check_in or self.request.GET['check_out']<check_in):
                context["error_message"]="Check in and check out date should be today or upcoming days."
                return context

            else:    
                print(type(self.request.GET['check_in']))
                context['rooms_list']=Rooms.objects.raw(f'''
                                                        Select * from rooms_rooms room where room.room_type="{self.request.GET['room_type']}" and room.room_no not in 
                                                        (
                                                            Select reservation.booked_room_id from rooms_reservation reservation, rooms_rooms roomobj
                                                            where reservation.booked_room_id=roomobj.room_no and
                                                            (reservation.booked_from>="{self.request.GET['check_in']}" and reservation.booked_till<="{self.request.GET['check_out']}")
                                                        )
                                                        ''')
                
                context['form']=RoomsSearchForm(initial={'check_in':self.request.GET['check_in'],
                                                    'check_out':self.request.GET['check_out'],
                                                    'room_type':self.request.GET['room_type']
                                                    })

                self.request.session['check_in']=self.request.GET['check_in']
                self.request.session['check_out']=self.request.GET['check_out']
                
                return context




class RoomDetailView(DetailView):
    model= Rooms
    template_name="users/roomdetail.html"

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        self.request.session["room_no"]=self.object.room_no       
        return context

class PaymentView(TemplateView):
    template_name="users/paymentreview.html"

    def post(self,request,*args,**kwargs):
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_amount=self.request.session["amount_payable"]*100
        razorpay_currency="INR"
        DATA = {
                "amount": razorpay_amount,
                "currency": razorpay_currency,
                "payment_capture":"1"
            }
        
        razorpay_order=razorpay_client.order.create(data=DATA)
        # print(razorpay_order)
        razorpay_order_id=razorpay_order["id"]
        razorpay_key_id=RAZORPAY_KEY_ID
        # self.request.session["razorpay_order_id"]=razorpay_order["id"]
        reservation=Reservation.objects.create(booked_room=Rooms.objects.get(room_no=self.request.session["room_no"]),
                                                booked_by=self.request.user,
                                                booked_from=self.request.session["check_in"],
                                                booked_till=self.request.session["check_out"],
                                                reservation_amount=self.request.session["amount_payable"],
                                                provider_order_id=razorpay_order_id)
        reservation.save()
        self.request.session["user_id"]=self.request.user.id
        return render(self.request,"users/sample_pay.html",locals())

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["room_obj"]=Rooms.objects.get(room_no=self.request.session["room_no"])
        context["user_obj"]=CustomUser.objects.get(id=self.request.user.id)
        
        context["check_in"]=self.request.session["check_in"]
        context["check_out"]=str(self.request.session["check_out"])
        context["no_of_days"]=(datetime.strptime(self.request.session['check_out'],"%Y-%m-%d")-datetime.strptime(self.request.session['check_in'],"%Y-%m-%d")).days
        context["amount_payable"]=context["room_obj"].room_price*context["no_of_days"]
        self.request.session["amount_payable"]=context["amount_payable"]

        return context

@csrf_exempt
def callback(request):
    subject="Reservation Confirmation"
    email_from=EMAIL_HOST_USER
    def verify_signature(response_data):
        print(response_data)
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        print("hii")
        print("it is here")
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        reservation = Reservation.objects.get(provider_order_id=provider_order_id)
        reservation.payment_id = payment_id
        reservation.signature_id = signature_id
        reservation.save()
        response_data={"razorpay_payment_id":payment_id,
                        "razorpay_order_id":provider_order_id,
                        "razorpay_signature":signature_id}
        if verify_signature(response_data):
            print("verified")
            reservation.reservation_status = ReservationStatus.RESERVED
            reservation.payment_status=PaymentStatus.SUCCESS
            reservation.save()            
            user=CustomUser.objects.get(email=reservation.booked_by)
            room=Rooms.objects.get(room_no=reservation.booked_room)
            message=f'''Hi {user.first_name},
                        We're glad to have you to choose our resort! 
                        Reservation Details
                        Customer Name: {user.first_name} {user.last_name}
                        Room No.: {room.room_no}
                        Check In Date: {reservation.booked_from}
                        Check Out Date: {reservation.booked_till}
                        Amount Paid: {reservation.reservation_amount}
                        Reservation Status: {ReservationStatus.RESERVED}
                        Payment Status: {PaymentStatus.SUCCESS}
                        '''
            recipient_list=[user.email,]
            send_mail(subject,message,email_from,recipient_list)
            return render(request, "users/callback.html", context={"status":reservation.payment_status})
        else:
            print("not verified")
            reservation.reservation_status = ReservationStatus.RESERVED
            reservation.payment_status=PaymentStatus.FAILURE
            reservation.save()
            message=f'''Hi {request.user.first_name},
                        We're glad to have you to choose our resort! 
                        Reservation Details
                        Customer Name: {request.user.first_name} {request.user.last_name}
                        Room No.: {request.session["room_no"]}
                        Check In Date: {request.session["check_in"]}
                        Check Out Date: {request.session["check_out"]}
                        Amount Paid: {request.session["amount_payable"]}
                        Reservation Status: {ReservationStatus.RESERVED}
                        Payment Status: {PaymentStatus.FAILURE}
                        '''
            recipient_list=[request.user.email,]
            send_mail(subject,message,email_from,recipient_list)
            return render(request, "users/callback.html", context={"status":reservation.payment_status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        reservation = Reservation.objects.get(provider_order_id=provider_order_id)
        reservation.payment_id = payment_id
        reservation.reservation_status=ReservationStatus.RESERVED
        reservation.payment_status = PaymentStatus.FAILURE
        message=f'''Hi {request.user.first_name},
                        We're glad to have you to choose our resort! 
                        Reservation Details
                        Customer Name: {request.user.first_name} {request.user.last_name}
                        Room No.: {request.session["room_no"]}
                        Check In Date: {request.session["check_in"]}
                        Check Out Date: {request.session["check_out"]}
                        Amount Paid: {request.session["amount_payable"]}
                        Reservation Status: {ReservationStatus.RESERVED}
                        Payment Status: {PaymentStatus.FAILURE}
                        '''
        recipient_list=[request.user.email,]
        send_mail(subject,message,email_from,recipient_list)
        reservation.save()
        return render(request, "users/callback.html", context={"status":reservation.payment_status})




#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# def homepage(request):
#     currency = 'INR'
#     amount = 20000  # Rs. 200
 
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
 
#     return render(request, 'users/indexpage.html', context=context)

# @csrf_exempt
# def paymenthandler(request):
 
#     # only accept POST request.
#     if request.method == "POST":
#         try:
           
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             if result is not None:
#                 amount = 20000  # Rs. 200
#                 try:
 
#                     # capture the payemt
#                     razorpay_client.payment.capture(payment_id, amount)
 
#                     # render success page on successful caputre of payment
#                     # return render(request, 'users/.html')
#                     return HttpResponse("Payment success")
#                 except:
 
#                     # if there is an error while capturing payment.
#                     return HttpResponse("Payment fail")
#             else:
 
#                 # if signature verification fails.
#                 return HttpResponse("Payment fail")
#         except:
 
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()


class SampleView(FormView):
    form_class=SampleForm
    template_name: str='users/sample.html'

    def get(self, request,*args,**kwargs):
        check_in_date="04/29/23"
        check_out_date="04/30/23"

        check_in = datetime.strptime(check_in_date, '%m/%d/%y').date()
        check_out = datetime.strptime(check_out_date, '%m/%d/%y').date()

        print(type(check_in))

        sample=Rooms.objects.raw(f'''Select * from rooms_rooms as room where room.room_type="Classic"''')
        
        # print(sample.query)

        # for sam in sample:
        #     print(sam.room_no,sam.room_type)


        # for samp in sample:
        #     print(check_in,">=",samp.booked_from,"=",check_in>=samp.booked_from)
        #     print(check_out,"<=",samp.booked_till,check_out<=samp.booked_till)
        # data=Reservation.objects.raw('''Select id,booked_room_id from rooms_reservation as reservation
        #                             ''')
        data=Reservation.objects.filter(booked_from__gte=check_in,booked_till__lte=str(check_out))
        print(data.query)
        for d in data:
            print(d.booked_room_id)
        # for room in data:
        #     print(room)

        return render(self.request,"users/sample.html",locals())


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


    # def get(self, request,*args, **kwargs) :
    #     setattr(self.request,'_mutable',True)
    #     self.request.GET['check_in']=date.today().strftime(("%Y-%m-%d"))
    #     self.request.GET['check_out']=(date.today()+dt.timedelta(days=1)).strftime("%Y-%m-%d")
    #     return self.request

    # def get_queryset(self) :
    #     print("hii")
    #     rooms_list=Rooms.objects.raw("select * from rooms_Rooms limit 2")
    #     # print(rooms_list)
    #     for room in Rooms.objects.raw("select * from rooms_Rooms"):
    #         print(room)
    #     return rooms_list