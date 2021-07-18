from django import forms
from django.forms import ModelForm
from .models import Room

class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['room_name']
