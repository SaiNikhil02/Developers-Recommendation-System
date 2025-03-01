from django.forms import ModelForm 
from .models import Project 

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_images', 'demo_link', 'source_link', 'tags']
        
    def validate_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise  forms.ValidationError("Description is too short")
        return description