from django.urls import path
from .views import dahsolar, overview, dah_factories, vission_mission

app_name = 'dahsolar'

urlpatterns = [
    path('', dahsolar, name="dahsolar"),
    path('overview/', overview, name="overview"),
    path('dah-factories/', dah_factories, name="dah-factories"),
    path('vission-mission/', vission_mission, name="vission-mission")
]