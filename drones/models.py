from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from djitellopy import TelloSwarm, Tello


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

    def swarm_takeoff(self):
        drones = Drone.objects.filter(swarm_ID=self)
        drone_ips = [drone.IP_address for drone in drones]
        print(drone_ips)
        drone_swarm = TelloSwarm.fromIps(drone_ips)
        drone_swarm.connect()
        drone_swarm.takeoff()
        drone_swarm.rotate_counter_clockwise(180)
        drone_swarm.land()
        drone_swarm.end()


class Drone(models.Model):
    drone_name = models.CharField(max_length=250)
    MAC_address = models.CharField(max_length=250, default='00:DE:AD:BE:EF:00')
    IP_address = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    swarm_ID = models.ForeignKey(Swarm, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete_command(self, request):
        custom_user = get_current_user(request)
        django_user = request.user
        custom_user.delete()
        django_user.delete()

    def get_battery(self):
        try:
            tello = Tello(host=self.IP_address)
            tello.connect()
            # Use this for working with mocked_drone
            state_packet = tello.get_current_state()
            print(state_packet)
            for key, value in state_packet.items():
                if key.strip() == 'bat':
                    battery_level = int(value.strip())
                    break
            # Use this for actual drone
            # battery_level = tello.get_battery()
        except Exception as e:
            print(f"Error retrieving battery level for drone {self.drone_name}: {e}")
            battery_level = -1

        battery_status = {
            'name': self.drone_name,
            'IP': self.IP_address,
            'MAC': self.MAC_address,
            'battery': battery_level
        }
        return JsonResponse(battery_status)


def get_latest_swarm():
    return Swarm.objects.last()


def get_current_user(request):
    return User.objects.get(username=request.user.username)


def get_next_drone_id(swarm):
    return Drone.objects.filter(swarm_ID=swarm).count() + 1


def add_default_drone(user, swarm):
    new_drone = Drone.objects.create(
        drone_name=f'Drone {get_next_drone_id(swarm)}',
        IP_address='127.0.0.1',
        updated_by=user,
        swarm_ID=swarm)


def add_default_swarm(user) -> Swarm:
    new_swarm = Swarm.objects.create(
        swarm_name='Swarm1',
        updated_by=user)
    return new_swarm


def crud_action(request, model, action):
    from drones.forms import UpdateDroneForm
    model_class = model_lookup[model][0]
    form_class = model_lookup[model][1]
    form = None

    if action == 'create':
        form = form_class(request.POST)
        if form.is_valid():
            new_instance = form.save(commit=False)
            new_instance.updated_by = get_current_user(request)
            if model_class == Drone:
                new_instance.swarm_ID = Swarm.objects.get(pk=request.POST.get('swarm'))
            new_instance.save()
    elif action == 'update':
        instance_id = request.POST.get('instance_id')
        instance = get_object_or_404(model_class, pk=instance_id)
        if model_class == Drone:
            form = UpdateDroneForm(request.POST, instance=instance)
        else:
            form = form_class(request.POST, instance=instance)
        if form.is_valid():
            updated_instance = form.save(commit=False)
            updated_instance.updated_by = get_current_user(request)
            updated_instance.save()
    elif action == 'delete':
        instance_id = request.POST.get('instance_id')
        try:
            instance = get_object_or_404(model_class, pk=instance_id)
            instance.delete()
        except TypeError as e:
            print(f"Deletion failed: {e}")
        except ValueError as e:
            print(f"Deletion failed: {e}")
    return form


from drones.forms import APForm, SwarmForm, DroneForm
model_lookup = {
    'ap': [AP, APForm],
    'swarm': [Swarm, SwarmForm],
    'drone': [Drone, DroneForm],
}
