from django.shortcuts import render, redirect
from .models import Profile, Skill, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles
# Create your views here.

def loginUser(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        print(request.POST)  # Debugging

        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '').strip()

        if not username:
            messages.error(request, 'Please enter a username')
            return render(request, 'users/login_register.html', context)

        if not password:
            messages.error(request, "Please enter a password")
            return render(request, 'users/login_register.html', context)

        # Use .filter().first() instead of try-except
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            messages.error(request, "Invalid Username")
            return render(request, 'users/login_register.html', context)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'account'))  # Safer redirect
        else:
            messages.error(request, "Invalid password")

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
    profiles, search_query = context = searchProfiles(request)
    context = {'profiles':profiles, 'search_query':search_query} 
    return render(request, 'users/profiles.html', context)
        
        

def userProfile(request, pk):
    profile = Profile.objects.get(id = pk) 
    topSkills = profile.skill_set.exclude(description__exact = "") 
    otherSkills = profile.skill_set.filter(description = "")
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context) 

@login_required(login_url = 'login')
def userAccount(request):
    profile = request.user.profile 
    skills  = profile.skill_set.all()  
    projects  = profile.project_set.all()  
    context  = {'profile': profile, 'skills':skills, 'projects': projects}
    return render(request,'users/account.html',context) 

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

@login_required(login_url = 'login')
def deleteSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted')
        return redirect('account')
    context  = {'object': skill} 
    return render(request, 'delete_template.html', context)

@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile 
    messageRequests = profile.messages.all() 
    unreadCount = messageRequests.filter(is_read = False).count() 
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)
    
@login_required(login_url = 'login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id = pk) 
    if not message.is_read:
        message.is_read = True 
        message.save()
    
    context = {'message': message}
    return render(request, 'users/message.html', context)
    
def createMessage(request, pk):
    recipient = Profile.objects.get(id = pk) 
    form = MessageForm() 
    try:
        sender =  request.user.profile 
    except:
        sender = None 
    if request.method == 'POST':
        form = MessageForm(request.POST) 
        if form.is_valid():
            message = form.save(commit = False) 
            message.sender = sender 
            message.recipient = recipient 
            if sender:
                message.name = sender.name 
                message.email = sender.email 
        
            message.save()
            messages.success(request, 'Your message was sucessfully sent')
            return redirect('profiles', pk = recipient.id)
    context = {'recipient': recipient, 'form': form} 
    return render(request, 'users/message_form.html', context)
    