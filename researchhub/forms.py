from django import forms
from django.contrib.auth.models import User

from researchhub import utils
from researchhub.models import Supervisor, Project, SkilledStudent

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['supervisor', 'field', 'title', 'description',
                  'required_role', 'prerequisites', 'duration',
                  'communication']

class MemberProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['supervisor', 'field', 'title', 'description',
                  'required_role', 'prerequisites', 'duration',
                  'communication', 'is_personal']

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['user', 'specialty', 'avatar', 'position',
                  'interests', 'communication', 'is_hidden',
                  'available_from', 'available_until']

class SkilledStudentForm(forms.ModelForm):
    class Meta:
        model = SkilledStudent
        fields = ['description', 'previous_experience',
                  'ongoing_projects', 'condition', 'available_until']
                  
