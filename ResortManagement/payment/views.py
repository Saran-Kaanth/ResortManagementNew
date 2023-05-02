from django.shortcuts import render
# from .models import Order
from django.views.decorators.csrf import csrf_exempt
import razorpay
from ResortManagement.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)
# from ResortManagement.config.settings.
# from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
# Create your views here.

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"

# RAZOR_KEY_ID="rzp_test_0Wa2w1hzK9igoP"
# RAZOR_KEY_SECRET="QZgVBHK9OL1j738fAxvAEAbb"

def home(request):
    return render(request, "users/index.html")

def order_payment(request):
    if request.method == "POST":
        print("hii")
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        print(razorpay_order)
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "users/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback/",
                "razorpay_key": RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    return render(request, "users/payment.html")

@csrf_exempt
def callback(request):
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
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        response_data={"razorpay_payment_id":payment_id,
                        "razorpay_order_id":provider_order_id,
                        "razorpay_signature":signature_id}
        if verify_signature(response_data):
            print("verified")
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "users/callback.html", context={"status":order.status})
        else:
            print("not verified")
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "users/callback.html", context={"status":order.status})
    else:
        print("hii")
        print(request.POST.get("error[metadata]"))
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "users/callback.html", context={"status":order.status})
