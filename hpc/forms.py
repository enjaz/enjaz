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
        fields = ['ar_name', 'en_name', 'email', 'mobile_number',
                  'university', 'college', 'gender']
        
class RegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
        time_slots = Session.objects.filter(time_slot__isnull=False).values_list('time_slot', flat=True).distinct()
        for time_slot in time_slots:
            time_slot_sessions = Session.objects.filter(time_slot=time_slot)
            if user:
                user_gender = get_user_gender(user)
                print user_gender
                time_slot_sessions = Session.objects.filter(time_slot=time_slot, gender__in=['', user_gender])
            self.fields['time_slot_%s' % time_slot] = forms.ModelChoiceField(time_slot_sessions, required=False)
            self.fields['time_slot_%s' % time_slot].widget.attrs['class'] = 'form-control'

        nontime_sessions = Session.objects.filter(time_slot__isnull=True)

        for nontime_session in nontime_sessions:
            self.fields['session_%s' % nontime_session.pk] = forms.BooleanField(label=nontime_session.name,
                                                                                required=False)

    def save(self, nonuser=None, user=None):
        if user:
            registration = Registration.objects.create(user=user)
        elif nonuser:
            registration = Registration.objects.create(nonuser=nonuser)
    
        timed_session_fields = [field_name for field_name in self.cleaned_data
                                if field_name.startswith('time_slot_')]
        untimed_session_pks = [int(field_name.split('_')[-1]) for field_name in self.cleaned_data
                               if field_name.startswith('session_') and self.cleaned_data[field_name]]

        # Everyone will be registered in the main track and the
        # resreach track:
        main_track = Session.objects.get(pk=1)
        registration.sessions.add(main_track)

        # Then we will add sessions added by the user.

        for timed_session_field in timed_session_fields:
            session = self.cleaned_data[timed_session_field]
            if session:
                registration.sessions.add(session)

        for session_pk in untimed_session_pks:
            session = Session.objects.get(pk=session_pk)
            registration.sessions.add(session)
