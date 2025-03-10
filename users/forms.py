
from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'email', 'username','password1', 'password2'] 
        labels = {'first_name': 'Name'} # so instead of first_name name will be displayed

class ProfileForm(ModelForm):
    class Meta:
        model =Profile
        fields = ['name', 'username', 'email', 'short_intro', 'bio', 'profile_image', 'social_github', 'social_linkedin'] 
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__' 
        exclude = ['owner']  
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'}) 
            
        
class MessageForm(ModelForm):
    class Meta:
        model = Message 
        fields = ['name', 'email', 'subject', 'body'] 
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})
    
    