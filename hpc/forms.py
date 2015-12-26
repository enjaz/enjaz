# -*- coding: utf-8  -*-
from django import forms

from accounts.utils import get_user_gender
from hpc.models import Abstract, Evaluation, NonUser, Session, Registration


default_choices = [(i, i) for i in range(1, 6)]

class AbstractForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ['title', 'authors', 'university', 'college',
                  'presenting_author', 'email', 'phone', 'level',
                  'presentation_preference', 'attachment']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['clear_objectives', 'informative_abstract',
                  'introduction', 'clear_method', 'good_statistics',
                  'clear_sampling', 'clear_results',
                  'clear_discussion', 'good_english',
                  'overall_evaluation']
        widgets = {field: forms.RadioSelect for field in fields}

class NonUserForm(forms.ModelForm):
    class Meta:
        model = NonUser
        fields = ['ar_first_name', 'ar_middle_name', 'ar_last_name',
                  'en_first_name', 'en_middle_name', 'en_last_name',
                  'email', 'mobile_number', 'university', 'college',
                  'gender']
        
class RegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        time_slots = Session.objects.filter(time_slot__isnull=False).values_list('time_slot', flat=True).distinct()
        for time_slot in time_slots:
            time_slot_sessions = Session.objects.filter(time_slot=time_slot)
            if user:
                user_gender = get_user_gender(user)
                time_slot_sessions = Session.objects.filter(time_slot=time_slot, gender__in=['', user_gender])
            self.fields['time_slot_%s' % time_slot] = forms.ModelChoiceField(time_slot_sessions, required=False)
            self.fields['time_slot_%s' % time_slot].widget.attrs['class'] = 'form-control'

        untimed_sessions = Session.objects.filter(time_slot__isnull=True)

        for untimed_session in untimed_sessions:
            self.fields['session_%s' % untimed_session.code_name] = forms.BooleanField(label=untimed_session.name,
                                                                                       required=False)

    def save(self, nonuser=None, user=None):    
        timed_session_fields = [field_name for field_name in self.cleaned_data
                                if field_name.startswith('time_slot_') and self.cleaned_data[field_name]]
        untimed_session_code_names = [field_name.split('_')[-1] for field_name in self.cleaned_data
                               if field_name.startswith('session_') and self.cleaned_data[field_name]]

        # If no sessions were selected, do not register.
        if not untimed_session_code_names and \
           not timed_session_fields:
            return

        if user:
            registration = Registration.objects.create(user=user)
        elif nonuser:
            registration = Registration.objects.create(nonuser=nonuser)

        for timed_session_field in timed_session_fields:
            session = self.cleaned_data[timed_session_field]
            if session:
                registration.sessions.add(session)

        for session_code_name in untimed_session_code_names:
            session = Session.objects.get(code_name=session_code_name)
            registration.sessions.add(session)
