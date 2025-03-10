from django.http import JsonResponse 
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import ProjectSerializer 
from projects.models import Project

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'}, 
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes) 

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all() 
    serializer =ProjectSerializer(projects, many = True)  #converts  query set to json and Model instance to json many = True means we are serializing multiple objects
    
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id = pk) 
    serializer =ProjectSerializer(project) 
    
    return Response(serializer.data)
    