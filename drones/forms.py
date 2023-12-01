from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import AP, Swarm, Drone


class APForm(forms.ModelForm):
    class Meta:
        model = AP
        fields = ['SSID', 'password', 'auth_method']

    def save(self, commit=True, *args, **kwargs):
        instance = super(APForm, self).save(commit=False, *args, **kwargs)
        instance.created_at = timezone.now()
        instance.updated_by = kwargs.get('user')
        if commit:
            instance.save()
        return instance


class SwarmForm(forms.ModelForm):
    class Meta:
        model = Swarm
        fields = '__all__'


class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['drone_name', 'IP_address']

    def __init__(self, *args, swarm_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['IP_address'].initial = '127.0.0.1'

        if swarm_id:
            swarm = get_object_or_404(Swarm, id=swarm_id)
            drone_count = Drone.objects.filter(swarm_ID=swarm_id).count()
            self.fields['drone_name'].initial = f'Drone {drone_count + 1}'
