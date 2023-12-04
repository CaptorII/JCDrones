from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import *
from .forms import *
from .sync_users import sync_users


def index(request):
    sync_users()  # call method to add custom users based on django users
    return render(request, "drones/index.html")


def update_email(request):
    user = User.objects.get(username=request.user.username)  # get user from request
    form = UserForm(instance=user)  # initialise form here so it can be passed to return

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)  # create form with details from POST request
        if form.is_valid():
            form.save()
    return render(request, 'drones/update_email.html', {'form': form})


def delete_user(request):
    if request.method == 'POST':
        custom_user = get_current_user(request)
        custom_user.delete_command(request)  # pass to model to delete user objects
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
    swarm = Swarm.objects.get(pk=request.POST.get('swarm_id'))
    swarm.swarm_takeoff()
    return render(request, "drones/dashboard.html")


def get_battery_status(request, drone_id):
    drone = Drone.objects.get(pk=drone_id)
    drone.get_battery()


def add_swarm(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request')
    user = get_current_user(request)
    new_swarm = add_default_swarm(user)  # pass to model to create new drone
    aps = AP.objects.all()
    ap_id = request.GET.get('ap_id')
    active_ap = get_object_or_404(AP, id=ap_id) if ap_id else None
    swarms = Swarm.objects.all()
    drones = Drone.objects.filter(swarm_ID=new_swarm)
    context = {'aps': aps, 'active_ap': active_ap, 'swarms': swarms, 'swarm': new_swarm, 'drones': drones}
    return render(request, 'drones/dashboard.html', context)


def add_drone(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request')
    swarm_id = request.POST.get('swarm_id')
    swarm = Swarm.objects.get(pk=swarm_id)
    user = get_current_user(request)
    add_default_drone(user, swarm)  # pass to model to create new drone
    aps = AP.objects.all()
    ap_id = request.GET.get('ap_id')
    active_ap = get_object_or_404(AP, id=ap_id) if ap_id else None
    swarms = Swarm.objects.all()
    drones = Drone.objects.filter(swarm_ID=swarm)
    context = {'aps': aps, 'active_ap': active_ap, 'swarms': swarms, 'swarm': swarm, 'drones': drones}
    return render(request, "drones/dashboard.html", context)


class CRUDView(View):
    template_name = 'drones/crud/crud_page.html'

    def get(self, request, model, *args, **kwargs):
        instances = model_lookup[model][0].objects.all()
        form = model_lookup[model][1]

        if model == 'drone':
            swarm_id = request.GET.get('swarm_id')
            form = DroneForm(swarm_id)

        return render(request, self.template_name, {'model': model, 'instances': instances, 'form': form})


class CRUDActionView(View):
    def post(self, request, model, action, *args, **kwargs):
        template_name = 'drones/crud/crud_page.html'
        form = crud_action(request, model, action)  # take actions within the model
        model_class = model_lookup[model][0]
        instances = model_class.objects.all()
        selected_instance_id = request.POST.get('instance_id')
        return render(request, template_name,
                      {'model': model, 'instances': instances, 'form': form, 'action': action, 'selected_instance_id': selected_instance_id})