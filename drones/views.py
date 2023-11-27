from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Swarm, Drone, User
from django.utils import timezone
from .sync_users import sync_users


def index(request):
    sync_users()
    return render(request, "drones/index.html")


def dashboard(request):
    swarm = get_swarm(request)
    context = {
        'swarm': swarm
    }
    return render(request, "drones/dashboard.html", context)


def add_swarm(request):
    if request.method == 'POST':
        username = request.user.username
        current_user = User.objects.get(username=username)
        new_swarm = Swarm(
            swarm_ID=0,
            swarm_name='Swarm1',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            updated_by=current_user
        )
        new_swarm.save()
        return redirect('dashboard')
    else:
        return HttpResponse('Invalid request')


def get_swarm(request) -> Swarm | None:
    latest_swarm = Swarm.objects.last()
    return latest_swarm


def add_drone(request):
    if request.method == 'POST':
        swarm_id = request.POST.get('swarm_id')
        swarm = get_object_or_404(Swarm, id=swarm_id)
        username = request.user.username
        current_user = User.objects.get(username=username)
        drone_count = Drone.objects.filter(swarm_ID=swarm_id).count()
        new_drone = Drone.objects.create(
            drone_ID=drone_count + 1,
            drone_name=f'Drone {drone_count + 1}',
            MAC_address='',
            IP_address='',
            created_by=current_user,
            updated_by=current_user,
            swarm_ID=swarm,
        )
        new_drone.save()
        return redirect('dashboard')
    else:
        return HttpResponse('Invalid request')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/../registration/templates/registration/signup.html"
