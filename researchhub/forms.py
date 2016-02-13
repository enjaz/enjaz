from django import forms
from django.contrib.auth.models import User

from accounts.models import CommonProfile
from core.models import StudentClubYear
from researchhub import utils
from researchhub.models import Supervisor, Project, SkilledStudent
from userena.forms import SignupForm


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
        fields = ['user', 'specialty', 'avatar', 'interests',
                  'communication', 'is_hidden', 'available_from',
                  'available_until']

class SkilledStudentForm(forms.ModelForm):
    class Meta:
        model = SkilledStudent
        fields = ['description', 'previous_experience',
                  'ongoing_projects', 'condition', 'available_until']

class ResearchHubSignupForm(SignupForm):
    city_choices = (
        ('R', u'Riyadh'),
        ('J', u'Jeddah'),
        ('A', u'Alahsa'),
    )

    en_first_name = forms.CharField(max_length=30)
    en_middle_name = forms.CharField(max_length=30)
    en_last_name = forms.CharField(max_length=30)
    badge_number = forms.IntegerField(required=False)
    job_description = forms.CharField(label=CommonProfile._meta.get_field('job_description').verbose_name,
                                       max_length=50)
    specialty = forms.CharField(max_length=100)
    interests = forms.CharField(widget=forms.Textarea)
    communication = forms.CharField(widget=forms.Textarea)
    available_from = forms.DateField(required=False)
    available_until = forms.DateField(required=False)
    city = forms.CharField(max_length=1,
                           widget=forms.Select(choices=city_choices))

    def __init__(self, *args, **kw):
        super(ResearchHubSignupForm, self).__init__(*args, **kw)
        # We don't want usernames (We could have inherited userena's
        # SignupFormOnlyEmail, but it's more tricky to modify.)
        del self.fields['username']

    def clean(self):
        # Call the parent class's clean function.
        cleaned_data = super(ResearchHubSignupForm, self).clean()

        # Remove spaces at the start and end of all text fields.
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()

        return cleaned_data

    def save(self):
        # All username names should be lower-case.
        self.cleaned_data['email'] = self.cleaned_data['email'].lower()
        self.cleaned_data['username'] = self.cleaned_data['email'].split('@')[0]
        self.cleaned_data['username'] = self.cleaned_data['username']
        new_user = super(ResearchHubSignupForm, self).save()
        current_year = StudentClubYear.objects.get_current()
        CommonProfile.objects.create(user=new_user,
                                     is_student=False,
                                     en_first_name=self.cleaned_data['en_first_name'],
                                     en_middle_name=self.cleaned_data['en_middle_name'],
                                     en_last_name=self.cleaned_data['en_last_name'],
                                     badge_number=self.cleaned_data['badge_number'],
                                     city=self.cleaned_data['city'],
                                     job_description=self.cleaned_data['job_description'],
                                     college=None,
                                     student_id=None)
        Supervisor.objects.create(user=new_user,
                                  year=current_year,
                                  interests=self.cleaned_data['interests'],
                                  communication=self.cleaned_data['communication'],
                                  specialty=self.cleaned_data['specialty'],
                                  available_from=self.cleaned_data.get('available_from'),
                                  available_until=self.cleaned_data.get('available_until'))
        return new_user
