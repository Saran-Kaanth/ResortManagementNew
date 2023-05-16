from django.views.generic import TemplateView
from ResortManagement.settings import (RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET,EMAIL_HOST_USER)
import razorpay
from django.views.decorators.csrf import csrf_exempt
from rooms.models import *
from users.models import *
from rooms.constants import *
import json
from django.core.mail import send_mail
from django.shortcuts import render
from datetime import datetime


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
        razorpay_order_id=razorpay_order["id"]
        razorpay_key_id=RAZORPAY_KEY_ID
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
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
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
            try:
                send_mail(subject,message,email_from,recipient_list)
            except:
                return render(request, "users/callback.html", context={"status":reservation.payment_status})
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
            try:
                send_mail(subject,message,email_from,recipient_list)
            except:
                return render(request, "users/callback.html", context={"status":reservation.payment_status})
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
        try:
            print("mail sent")
            send_mail(subject,message,email_from,recipient_list)
        except:
            return render(request, "users/callback.html", context={"status":reservation.payment_status})
        return render(request, "users/callback.html", context={"status":reservation.payment_status})
