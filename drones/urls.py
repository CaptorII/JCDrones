from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add_swarm/", views.add_swarm, name="add_swarm"),
    path("add_drone/", views.add_drone, name="add_drone"),
    path('crud/<str:model>/', views.CRUDView.as_view(), name='crud'),
    path('crud/<str:model>/<str:action>/', views.CRUDActionView.as_view(), name='crud_action'),
]
