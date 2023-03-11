from django.shortcuts import render, get_object_or_404
from projects.models import Project

# Create your views here.
def projects(request):
    projects=Project.actives.all()
    context={
        'projects': projects
    }
    return render(request, "projects/home.html", context=context)
def project_item(request, id):
    item=get_object_or_404(Project, id=id)
    context={
        'item': item
    }
    return render(request, "projects/item.html", context=context)