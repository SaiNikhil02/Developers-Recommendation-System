from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required

def projects(request):
    return render(request, 'projects.html')
# Create your views here.
@login_required(login_url = 'login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm() 
    if request.method =='POST':
        print(request.POST)
        form = ProjectForm(request.POST) 
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile 
            project.save() 
            return redirect('projects')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context) 

@login_required(login_url = 'login')
def updateProject(request, pk):
    profile = request.user.profile 
    project = profile.project_set.get(id = pk) 
    project = Project.objects.get(id=pk) 
    form = ProjectForm(instance = project)
    
    if request.method =='POST':
        print(request.POST)
        form = ProjectForm(request.POST, instance = project) 
        if form.is_valid():
            form.save()
            return redirect('projects')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url = 'login')
def deleteProject(request, pk):
    profile = request.user.profile 
    project = profile.project_set.get(id = pk) 
    
    if request.method == 'POST':
        project.delete() 
        redirect('projects') 
        
    context ={'object':'pk'} 
    return render(request, 'projects/delete_template.html', context)
    
    
    
