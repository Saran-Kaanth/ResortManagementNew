from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.urls import reverse


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username=models.TextField(max_length=150,null=False,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    gender_choices=(('Male','Male'),
                    ('Female','Female'),
                    ('Gender','-'))
    
    first_name=models.TextField(max_length=150,null=False,blank=False)
    last_name=models.TextField(max_length=150,null=True,blank=True)
    gender=models.TextField(choices=gender_choices,default='Gender',max_length=30)
    age=models.IntegerField(default=0)
    flat_no=models.TextField(max_length=200,blank=True,null=False)
    area=models.TextField(max_length=300,blank=True,null=False,default='')
    city=models.TextField(max_length=200,default='')
    state=models.TextField(max_length=200,default='')
    pincode=models.IntegerField(blank=True, null=True)
    mobile=models.TextField(max_length=10,default='')
    DisplayFields=['email','first_name','last_name','gender','age','pincode']

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("userprofile",kwargs={"pk":self.pk})
    
# class Rooms(models.Model):
#     room_no=models.AutoField(primary_key=True)
#     room_type=models.TextField(max_length=200)
#     room_price=models.IntegerField(default=0)
#     # room_status=models.TextField(max_length=200)
#     room_available=models.BooleanField(default=True)
    
# class Reservation(models.Model):
#     reservation_choices=(('Check In','Checked In'),
#                          ('Check Out','Checked Out'),
#                         ('Hold','On Hold'))
    
#     booked_room=models.OneToOneField(Rooms, verbose_name=_("Room No"), on_delete=models.CASCADE,blank=True)
#     booked_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     reservation_status=models.TextField(max_length=40,choices=reservation_choices,default='On Hold')
    
#     def __str__(self):
#         return str(self.booked_room)

