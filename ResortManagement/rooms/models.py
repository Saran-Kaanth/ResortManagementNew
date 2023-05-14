# from datetime import datetime
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from  users.models import CustomUser
from .constants import *



# Create your models here.
class Rooms(models.Model):
    room_type_choices=(("Premium","Premium"),
                        ("Classic","Classic"),
                        ("Cottage","Cottage"))
    room_no=models.CharField(primary_key=True,verbose_name=_('Room No'),max_length=10)
    room_type=models.TextField(choices=room_type_choices,default="Classic",max_length=30)
    room_price=models.FloatField(default=0)
    # room_status=models.TextField(max_length=200)
    room_available=models.BooleanField(default=True)
    DisplayFields=['room_no','room_type','room_price','room_available']

    def __str__(self):
        return str(self.room_no)
    
    def get_absolute_url(self):
        return reverse("room_detail",kwargs={"pk":self.pk})

class Reservation(models.Model):
    booked_room=models.ForeignKey(Rooms, on_delete=models.CASCADE,blank=True)
    booked_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    booked_from=models.DateField(verbose_name=_("Check In Date"),default=datetime.date.today)
    booked_till=models.DateField(verbose_name=_("Check Out Date"),default=datetime.date.today)
    reservation_amount=models.FloatField(verbose_name=_("Amount Paid"),default=0)
    reservation_status=models.CharField(
        _("Reservation Status"),
        default=ReservationStatus.RESERVED,
        max_length=254,
        blank=False,
        null=False,
    )
    payment_status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False,default=""
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False,default=""
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False,default=""
    )
    DisplayFields=['booked_room','booked_by','booked_from','booked_till','payment_status','reservation_status']

    
    def __str__(self):
        return str(self.booked_room)

    def get_absolute_url(self):
        return reverse("reservation_detail",kwargs={"pk":self.pk})

class RoomFeedback(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True)
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE,blank=True)
    room_rating=models.IntegerField(default=0)
    resort_rating=models.IntegerField(default=0)
    feedback=models.TextField(max_length=400,blank=False,null=False,default='')

    def __str__(self):
        return f"{self.room.room_no}: {self.room_rating}"

    def absolute_url(self):
        return reverse("room_feedback",kwargs={"pk":self.pk})
    


