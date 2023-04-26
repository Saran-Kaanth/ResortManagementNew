# from datetime import datetime
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from  users.models import CustomUser

# Create your models here.
class Rooms(models.Model):
    room_type_choices=(("Premium","Premium"),
                        ("Classic","Classic"),
                        ("Cottage","Cottage"))
    room_no=models.CharField(primary_key=True,verbose_name=_('Room No'),max_length=10)
    room_type=models.TextField(choices=room_type_choices,default="Classic",max_length=30)
    room_price=models.IntegerField(default=0)
    # room_status=models.TextField(max_length=200)
    room_available=models.BooleanField(default=True)
    DisplayFields=['room_no','room_type','room_price','room_available']

    def __str__(self):
        return str(self.room_no)
    
    def get_absolute_url(self):
        return reverse("room_detail",kwargs={"pk":self.pk})

class Reservation(models.Model):
    reservation_choices=(('Check In','Checked In'),
                         ('Check Out','Checked Out'),
                        ('Hold','On Hold'))

    
    booked_room=models.OneToOneField(Rooms, on_delete=models.CASCADE,blank=True)
    booked_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    booked_from=models.DateField(verbose_name=_("Check In Date"),default=datetime.date.today)
    booked_till=models.DateField(verbose_name=_("Check Out Date"),default=datetime.date.today)
    reservation_status=models.TextField(max_length=40,choices=reservation_choices,default='On Hold')
    DisplayFields=['booked_room','booked_by','booked_from','booked_till','reservation_status']

    
    def __str__(self):
        return str(self.booked_room)

    def get_absolute_url(self):
        return reverse("reservation_detail",kwargs={"pk":self.pk})