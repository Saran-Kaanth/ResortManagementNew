from django import forms
from .models import *
from django.forms.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from django.forms import TextInput, EmailInput,NumberInput,PasswordInput,RadioSelect   

class RoomsCreationForm(forms.ModelForm):
    class Meta:
        model=Rooms
        fields="__all__"



class RoomsSearchForm(forms.Form):
    room_type_choices=(("Premium","Premium"),
                        ("Classic","Classic"),
                        ("Cottage","Cottage"))
    check_in=forms.DateField(widget=forms.widgets.DateInput(attrs={
                'type': 'date', 'placeholder': datetime.datetime.today,
                'style': 'max-width: 300px;',
                'class':'form-control'
                }))
    check_out=forms.DateField(widget=forms.widgets.DateInput(attrs={
                'type': 'date', 'placeholder': datetime.datetime.today,
                'style': 'max-width: 300px;',
                'class':'form-control'
                }))
    room_type=forms.ChoiceField(choices=room_type_choices)

# class RoomFeedBackForm(forms.ModelForm):
#     class Meta:
#         model=RoomFeedback
#         fields=('room_rating','resort_rating','feedback',)


class SampleForm(forms.Form):
    name=forms.CharField(max_length=10)
    age=forms.IntegerField()


