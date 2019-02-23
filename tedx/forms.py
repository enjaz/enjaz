from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name','gender','age','mobile','emial','city','job_title','about_tedx','attend_tedx',
                  'expectations','work_place']
