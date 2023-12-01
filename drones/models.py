from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250)


class AP(models.Model):
    SSID = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    auth_method = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Swarm(models.Model):
    swarm_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Drone(models.Model):
    drone_name = models.CharField(max_length=250)
    MAC_address = models.CharField(max_length=250, default='00:DE:AD:BE:EF:00')
    IP_address = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    swarm_ID = models.ForeignKey(Swarm, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
