from django.db import models
import uuid
from users.models import Profile
# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null = True, blank = True, on_delete = models.SET_NULL)
    title = models.CharField(max_length=200) 
    description = models.TextField(null = True, blank = True) 
    featured_images = models.ImageField(null = True, blank = True, default = "images/default.jpg", max_length = 2000)
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    source_link = models.URLField(null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank = True) 
    vote_total = models.IntegerField(default = 0, null = True, blank = True) 
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True) 
    id = models.UUIDField(default = uuid.uuid4, unique =True, primary_key = True, editable  = False) 
    
    def __str__(self):
        return self.title 
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
    
     
