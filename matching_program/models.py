from django.db import models
from django.contrib.auth.models import User

research_status=(
        ('A','applied'),
        ('N','new'),
        ('IP', 'in progress'),
        ('P', 'puplished'),
        )

class Field(models.Model):
    name= models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Skills(models.Model):
    name= models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class ResearchProject(models.Model):
    creator= models.ForeignKey(User,
                             related_name="creator")
    members= models.ManyToManyField(User,
                                    related_name="members",
                                    blank=True,
                                    verbose_name='members',
                                    )
    field= models.ForeignKey(Field,
                             verbose_name='field',
                             null=True)
    supervisor= models.CharField(max_length=100,
                                 verbose_name="Supervisor's name")
    title= models.CharField(max_length=100)
    description= models.TextField()
    required_role= models.CharField(max_length=100)
    status= models.CharField(choices= research_status, default='A',
                             max_length=10)
    communication= models.TextField()
    date= models.DateTimeField(auto_now_add=True)

    def update_project(self, request):
        self.supervisor = request.POST.get('supervisor')
        self.title = request.POST.get('title')
        self.description = request.POST.get('description')
        self.required_role = request.POST.get('required_role')
        self.communication = request.POST.get('communication')
        self.save()

        
    def __unicode__(self):
        return self.title

    
class StudentApplication(models.Model):
    user= models.ForeignKey(User, related_name="user")
    research= models.ForeignKey(ResearchProject)
    skills= models.ManyToManyField(Skills)
    experience= models.TextField()
    advantages= models.TextField(verbose_name="Why we should pick you?")
    date= models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.user)
    
# Create your models here.
