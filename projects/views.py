from django.shortcuts import render, get_object_or_404
from projects.models import Project
def base(request):
    services=Project.services.all()
    projects=Project.actives.all()
    context={
        'services': services,
        'projects': projects
    }
    if projects.get(id=1).application_id is not "":
        print(projects.get(id=1).application_id)
    return render(request, "base.html", context=context)
# Create your views here.
def projects(request):
    projects=Project.actives.all()
    context={
        'projects': projects
    }
    return render(request, "projects/home.html", context=context)
def services(request):
    services=Project.services.all()
    context={
        'services': services
    }
    return render(request, "base.html", context=context)
def project_item(request, id):
    item=get_object_or_404(Project, id=id)
    context={
        'item': item
    }
    return render(request, "projects/item.html", context=context)