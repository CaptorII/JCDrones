from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic, View
from .models import Swarm, Drone, User, AP
from .forms import APForm, SwarmForm, DroneForm
from django.utils import timezone
from .sync_users import sync_users


def index(request):
    sync_users()
    return render(request, "drones/index.html")


def dashboard(request):
    swarm = get_latest_swarm()
    context = {'swarm': swarm}
    return render(request, "drones/dashboard.html", context)


def add_swarm(request):
    if request.method == 'POST':
        user = get_current_user(request)
        new_swarm = Swarm(
            swarm_name='Swarm1',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            updated_by=user)
        new_swarm.save()
        return redirect('dashboard')
    else:
        return HttpResponse('Invalid request')


def get_latest_swarm():
    return Swarm.objects.last()


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
        drones = Drone.objects.filter(swarm_ID=swarm)
        return render(request, 'drones/dashboard.html', {'swarm': swarm, 'drones': drones})
    else:
        return HttpResponse('Invalid request')


def get_current_user(request):
    return User.objects.get(username=request.user.username)


def get_next_drone_id(swarm):
    return Drone.objects.filter(swarm_ID=swarm).count() + 1


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/../registration/templates/registration/signup.html"


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
            form = DroneForm(swarm_id=swarm_id)
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
                    form.save()
                elif action == 'update':
                    instance = get_object_or_404(model_class, pk=instance_id)
                    form = form_class(request.POST, instance=instance)
                    form.save()
                elif action == 'delete':
                    instance = get_object_or_404(model_class, pk=instance_id)
                    instance.delete()
                return redirect('crud', model=model)

        instances = model_class.objects.all()
        return render(request, self.template_name,
                      {'model': model, 'instances': instances, 'form': form, 'action': action})
