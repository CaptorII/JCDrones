from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from . import views
from .models import AP, Swarm, Drone


class APForm(forms.ModelForm):
    class Meta:
        model = AP
        fields = ['SSID', 'password', 'auth_method']


class SwarmForm(forms.ModelForm):
    class Meta:
        model = Swarm
        fields = ['swarm_name']


class DroneForm(forms.ModelForm):
    swarm = forms.ModelChoiceField(queryset=Swarm.objects.all(), label='Select Swarm')

    class Meta:
        model = Drone
        fields = ['drone_name', 'IP_address']
