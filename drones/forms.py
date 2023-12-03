from django import forms
from .models import User, AP, Swarm, Drone


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


class UpdateDroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['drone_name', 'IP_address']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
