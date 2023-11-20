from django.db import models


class Users(models.Model):
    user_ID = models.IntegerField(default=0)
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250)


class AP(models.Model):
    APID = models.IntegerField()
    SSID = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    auth_method = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Swarms(models.Model):
    swarm_ID = models.IntegerField(default=0)
    swarm_name = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Drones(models.Model):
    drone_ID = models.IntegerField()
    drone_name = models.CharField(max_length=250)
    MAC_address = models.CharField(max_length=250)
    IP_address = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    swarm_ID = models.ForeignKey(Swarms, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Users, on_delete=models.CASCADE)
