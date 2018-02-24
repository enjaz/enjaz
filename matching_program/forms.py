from django import forms
from django.contrib.auth.models import User

from accounts.models import CommonProfile
from matching_program import utils
from models import ResearchProject, StudentApplication



class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = ['title','supervisor','description','field',
                  'required_role','communication']

     
 

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = ['skills','experience', 'advantages']


