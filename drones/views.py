from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from djitellopy import Tello
from .models import Swarm, Drone, User, AP
from .forms import APForm, SwarmForm, DroneForm, UpdateDroneForm, UserForm
from .sync_users import sync_users


def index(request):
    sync_users()
    return render(request, "drones/index.html")


def update_email(request):
    user = User.objects.get(username=request.user.username)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    return render(request, 'drones/update_email.html', {'form': form})


def delete_user(request):
    if request.method == 'POST':
        custom_user = get_current_user(request)
        custom_user.delete()
        user = request.user
        user.delete()
        logout(request)
    return redirect('index')


def dashboard(request):
    aps = AP.objects.all()
    ap_id = request.GET.get('ap_id')
    active_ap = get_object_or_404(AP, id=ap_id) if ap_id else None
    swarms = Swarm.objects.all()
    swarm = get_latest_swarm()
    drones = Drone.objects.filter(swarm_ID=swarm)
    context = {'aps': aps, 'active_ap': active_ap, 'swarms': swarms, 'swarm': swarm, 'drones': drones}
    return render(request, "drones/dashboard.html", context)


def takeoff(request):
    drone = Drone.objects.get(pk=request.POST.get('drone_id'))
    tello = Tello(drone.IP_address)
    tello.connect()
    tello.takeoff()
    tello.rotate_counter_clockwise(180)
    tello.land()
    return render(request, "drones/dashboard.html")


def get_battery_status(request, drone_id):
    drone = Drone.objects.get(pk=drone_id)

    try:
        tello = Tello(host=drone.IP_address)
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
        print(f"Error retrieving battery level for drone {drone.drone_name}: {e}")
        battery_level = -1

    battery_status = {
        'name': drone.drone_name,
        'IP': drone.IP_address,
        'MAC': drone.MAC_address,
        'battery': battery_level
    }
    return JsonResponse(battery_status)


def get_latest_swarm():
    return Swarm.objects.last()


def get_current_user(request):
    return User.objects.get(username=request.user.username)


def get_next_drone_id(swarm):
    return Drone.objects.filter(swarm_ID=swarm).count() + 1


def add_swarm(request):
    if request.method == 'POST':
        user = get_current_user(request)
        new_swarm = Swarm.objects.create(
            swarm_name='Swarm1',
            updated_by=user)
        aps = AP.objects.all()
        ap_id = request.GET.get('ap_id')
        active_ap = get_object_or_404(AP, id=ap_id) if ap_id else None
        swarms = Swarm.objects.all()
        drones = Drone.objects.filter(swarm_ID=new_swarm)
        context = {'aps': aps, 'active_ap': active_ap, 'swarms': swarms, 'swarm': new_swarm, 'drones': drones}
        return render(request, 'drones/dashboard.html', context)
    else:
        return HttpResponse('Invalid request')


def add_drone(request):
    if request.method == 'POST':
        swarm_id = request.POST.get('swarm_id')
        swarm = Swarm.objects.get(pk=swarm_id)
        user = get_current_user(request)
        new_drone = Drone.objects.create(
            drone_name=f'Drone {get_next_drone_id(swarm)}',
            IP_address='127.0.0.1',
            updated_by=user,
            swarm_ID=swarm)
        aps = AP.objects.all()
        ap_id = request.GET.get('ap_id')
        active_ap = get_object_or_404(AP, id=ap_id) if ap_id else None
        swarms = Swarm.objects.all()
        drones = Drone.objects.filter(swarm_ID=swarm)
        context = {'aps': aps, 'active_ap': active_ap, 'swarms': swarms, 'swarm': swarm, 'drones': drones}
        return render(request, "drones/dashboard.html", context)
    else:
        return HttpResponse('Invalid request')


class CRUDView(View):
    template_name = 'drones/crud/crud_page.html'

    def get(self, request, model, *args, **kwargs):
        instances = None
        form = None

        if model == 'ap':
            instances = AP.objects.all()
            form = APForm()
        elif model == 'swarm':
            instances = Swarm.objects.all()
            form = SwarmForm()
        elif model == 'drone':
            swarm_id = request.GET.get('swarm_id')
            form = DroneForm(swarm_id)
            instances = Drone.objects.all()

        return render(request, self.template_name, {'model': model, 'instances': instances, 'form': form})


class CRUDActionView(View):
    template_name = 'drones/crud/crud_page.html'

    def post(self, request, model, action, *args, **kwargs):
        form = None

        if model == 'ap':
            form_class = APForm
            model_class = AP
        elif model == 'swarm':
            form_class = SwarmForm
            model_class = Swarm
        elif model == 'drone':
            form_class = DroneForm
            model_class = Drone

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
            except Exception as e:
                print(f"Deletion failed: {e}")

        instances = model_class.objects.all()
        selected_instance_id = request.POST.get('instance_id')
        return render(request, self.template_name,
                      {'model': model, 'instances': instances, 'form': form, 'action': action, 'selected_instance_id': selected_instance_id})
