from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_manage.models import Project

@login_required
def mange(request):
    """
    接口管理
    """
    project_list = Project.objects.all()
    return render(request, "manage.html", {"projects": project_list})
