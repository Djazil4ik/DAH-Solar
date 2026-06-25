#dahsolar/views.py
from django.shortcuts import render

def dahsolar(request):
    return render(request, 'dahsolar/dahsolar.html')

def overview(request):
    return render(request, 'dahsolar/overview.html')

def dah_factories(request):
    return render(request, 'dahsolar/dah-factories.html')

def vission_mission(request):
    return render(request, 'dahsolar/vission-mission.html')