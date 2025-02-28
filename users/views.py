from django.shortcuts import render, redirect
from .models import Profile, Skill
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
# Create your views here.

def loginUser(request):
    page = 'register'
    context = {'page': page} 
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '')
        if username:
            try:
                user_obj = User.objects.get(username=username)
                password = request.POST.get('password', '')
                if password:
                    user = authenticate(request, username=username, password=password)
                    if user:
                        login(request, user)
                        return redirect('edit-account')
                    else:
                        messages.error(request, "Invalid password")
                else:
                    messages.error(request, "Please enter a password")
            except User.DoesNotExist:
                messages.error(request, "Invalid Username")
        else:
            messages.error(request, 'Please enter a username')
        
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request) 
    messages.info(request, "User logged out")
    return redirect('login') 

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm() 
    if request.method =='POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False) 
            user.username = user.username.lower() 
            user.save() 
            messages.success(request, 'User account created') 
            login(request, user) 
            return redirect('login')
        else:
            messages.error(request, 'An error has occurred during registration')
        
               
    context = {'page': page, 'form': form} 
    return render(request, 'users/login_register.html', context)
    

    
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html', context) 

def userProfile(request, pk):
    return render(request, 'users/user-profile.html') 

@login_required(login_url = 'login')
def userAccount(request):
    profile = request.user.profile 
    skills  = profile.skill_set.all()  
    projects  = Profile.project_set.all()  
    context  = {'profile': profile, 'skills':skills, 'projects': projects}
    return render(request,'users/account/html',context) 

@login_required(login_url = 'login')
def editAccount(request):
     form = ProfileForm() 
     if request.method =='POST':
         form = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
         if form.is_valid():
             form.save() 
             return redirect('account') 
         
         
     context  = {'form': form} 
     return render(request, 'users/profile_form.html', context) 
 
@login_required(login_url = 'login') 
def createSkill(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.save()
            messages.success(request, 'Skill added')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

 
@login_required(login_url = 'login') 
def updateSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id = pk)
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated')
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

def deleteSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted')
        return redirect('account')
    context  = {'object': skill} 
    return render(request, 'delete_template.html', context)
    