from django.contrib import admin

from .models import User, AP, Swarm, Drone

admin.site.register(User)
admin.site.register(AP)
admin.site.register(Swarm)
admin.site.register(Drone)
