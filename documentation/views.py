from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
from .models import method, interface, project
from time import gmtime, strftime

@login_required
def all_interfaces(request):
    all_interfaces = interface.objects.all()
    current_time = strftime("%a, %d %b %Y", gmtime())
    return render(request, 'all_interfaces.html', {'interfaces': all_interfaces, 'time': current_time})

@login_required
def view_interface(request, pk):
    curr_interface = get_object_or_404(interface, pk=pk)
    methods = curr_interface.methods.all()
    return render(request, 'interface.html', {'interface': curr_interface, 'methods': methods})

@login_required
def all_projects(request):
    all_projects = project.objects.all()
    return render(request, 'all_projects.html', {'projects': all_projects})

@login_required
def view_project_interfaces(request, pk):
    curr_project = get_object_or_404(project, pk=pk)
    all_interfaces = curr_project.interfaces.all()
    return render(request, 'view_project_interfaces.html', {'interfaces': all_interfaces, 'project': project})
