from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Swarm, Drone, User, AP
from .forms import APForm, SwarmForm, DroneForm
from .sync_users import sync_users


def index(request):
    sync_users()
    return render(request, "drones/index.html")


def dashboard(request):
    aps = AP.objects.all()
    ap_id = request.GET.get('ap_id')
    active_ap = get_object_or_404(AP, id=ap_id) if ap_id else None
    swarms = Swarm.objects.all()
    swarm = get_latest_swarm()
    drones = Drone.objects.filter(swarm_ID=swarm)
    context = {'aps': aps, 'active_ap': active_ap, 'swarms': swarms, 'swarm': swarm, 'drones': drones}
    return render(request, "drones/dashboard.html", context)


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

        if action in ('create', 'update', 'delete'):
            form = form_class(request.POST)
            if form.is_valid():
                instance_id = request.POST.get('instance_id')
                if action == 'create':
                    new_instance = form.save(commit=False)
                    new_instance.updated_by = get_current_user(request)
                    new_instance.save()
                elif action == 'update':
                    instance = get_object_or_404(model_class, pk=instance_id)
                    form = form_class(request.POST, instance=instance)
                    if form.is_valid():
                        updated_instance = form.save(commit=False)
                        updated_instance.updated_by = get_current_user(request)
                        updated_instance.save()
                elif action == 'delete':
                    instance = get_object_or_404(model_class, pk=instance_id)
                    instance.delete()
                    print("delete complete")

        instances = model_class.objects.all()
        return render(request, self.template_name,
                      {'model': model, 'instances': instances, 'form': form, 'action': action})
