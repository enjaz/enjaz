from django.db import models


class Events(models.Model):
    activity= models.ForeignKey('Activity')
    
    
    submission_date= models.DateField(verbose_name= "Envent date")
    start_time= models.TimeField(verbose_name= "Starting time")
    end_time= models.TimeField(verbose_name= "Ending time")
    name= models.CharField(max_length=200, verbose_name= "Event name")
    location= models.CharField(max_length=128, verbose_name= "Event location")
    short_description= models.CharField(max_length=128, verbose_name= "Short description of the event")
 

    
# Create your models here.
