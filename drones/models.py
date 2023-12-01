from django.db import models
from django.utils import timezone


class User(models.Model):
    user_ID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250)
    email = models.CharField(max_length=250)


class AP(models.Model):
    APID = models.AutoField(primary_key=True)
    SSID = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    auth_method = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.APID:
            ap_count = AP.objects.count()
            self.APID = ap_count + 1
        if not self.updated_by:
            self.updated_by = kwargs.get('user')
        self.updated_at = timezone.now()
        return super(AP, self).save(*args, **kwargs)


class Swarm(models.Model):
    swarm_ID = models.AutoField(primary_key=True)
    swarm_name = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Drone(models.Model):
    drone_ID = models.AutoField(primary_key=True)
    drone_name = models.CharField(max_length=250)
    MAC_address = models.CharField(max_length=250)
    IP_address = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    swarm_ID = models.ForeignKey(Swarm, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
