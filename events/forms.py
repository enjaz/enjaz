0# -*- coding: utf-8  -*-
from django import forms

from accounts.utils import get_user_gender
from events.models import NonUser, Session, Registration

class NonUserForm(forms.ModelForm):
    class Meta:
        model = NonUser
        fields = ['ar_first_name', 'ar_middle_name', 'ar_last_name',
                  'en_first_name', 'en_middle_name', 'en_last_name',
                  'email', 'mobile_number', 'university', 'college',
                  'gender']
        
class RegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.event = kwargs.pop("event")
        super(RegistrationForm, self).__init__(*args, **kwargs)
        time_slots = Session.objects.filter(event=self.event, time_slot__isnull=False).values_list('time_slot', flat=True).distinct()
        for time_slot in time_slots:
            time_slot_sessions = Session.objects.filter(event=self.event, time_slot=time_slot)
            if self.user:
                user_gender = get_user_gender(self.user)
                time_slot_sessions = Session.objects.filter(event=self.event,
                                                            time_slot=time_slot,
                                                            gender__in=['', user_gender])
            # Add as many time slot fields as many priorities we have.
            for priority in range(1, self.event.priorities + 1):
                self.fields['time_slot_%s_%s' % (time_slot, priority)] = forms.ModelChoiceField(time_slot_sessions, required=False)
                self.fields['time_slot_%s_%s' % (time_slot, priority)].widget.attrs['class'] = 'form-control'

        untimed_sessions = Session.objects.filter(event=self.event, time_slot__isnull=True)

        for untimed_session in untimed_sessions:
            print 'session_%s' % untimed_session.code_name
            self.fields['session_%s' % untimed_session.code_name] = forms.BooleanField(label=untimed_session.name,
                                                                                       required=False)

    def save(self, nonuser=None):
        timed_session_fields = [field_name for field_name in self.cleaned_data
                                if field_name.startswith('time_slot_') and self.cleaned_data[field_name]]
        untimed_session_code_names = [field_name.split('_')[-1] for field_name in self.cleaned_data
                               if field_name.startswith('session_') and self.cleaned_data[field_name]]

        # If no sessions were selected, do not register.
        if not untimed_session_code_names and \
           not timed_session_fields:
            print "fuck!"
            return

        if self.user:
            registration = Registration.objects.create(user=self.user)
        elif nonuser:
            registration = Registration.objects.create(nonuser=nonuser)

        for timed_session_field in timed_session_fields:
            session = self.cleaned_data[timed_session_field]
            if session:
                if timed_session_field.endswith("_1"):
                    registration.first_priority_sessions.add(session)
                elif timed_session_field.endswith("_2"):
                    registration.second_priority_sessions.add(session)

        for session_code_name in untimed_session_code_names:
            session = Session.objects.get(event=self.event, code_name=session_code_name)
            registration.first_priority_sessions.add(session)

        return registration
