from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from .models import Swarm, Drone
from django.utils import timezone


def index(request):
    return render(request, "drones/index.html")


def dashboard(request):
    return render(request, "drones/dashboard.html")


def add_swarm(request):
    if request.method == 'POST':
        user = request.user
        new_swarm = Swarm(
            swarm_ID=0,
            swarm_name='Swarm1',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            updated_by=user
        )
        new_swarm.save()
        return JsonResponse({'message': 'Swarm added successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_swarm(request):
    latest_swarm = Swarm.objects.last()

    if latest_swarm:
        swarm_details = {
            'swarm_name': latest_swarm.swarm_name
        }
        return JsonResponse({'swarm': swarm_details}, status=200)
    else:
        return JsonResponse({'swarm': None}, status=404)


def add_drone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        swarm_id = data.get('swarm_id')
        swarm = Swarm.objects.get(pk=swarm_id)

        user = request.user
        drone_count = Drone.objects.filter(swarm_ID=swarm).count()
        new_drone = Drone(
            drone_ID=drone_count + 1,
            drone_name=f'Drone {drone_count + 1}',
            MAC_address='',  # default MAC address
            IP_address='',
            created_at=timezone.now(),
            updated_at=timezone.now(),
            swarm_ID=swarm,
            updated_by=user
        )
        new_drone.save()
        return JsonResponse({'message': 'Drone added successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/../registration/templates/registration/signup.html"
