0# -*- coding: utf-8  -*-
from django import forms

from accounts.utils import get_user_gender
from events.models import NonUser, Session, Registration, Abstract, AbstractFigure
from django.forms.models import inlineformset_factory

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

class AbstractForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ['title', 'authors', 'university', 'college',
                  'study_field', 'presenting_author', 'email',
                  'phone', 'level', 'presentation_preference',
                  'introduction','methodology', 'results',
                  'discussion', 'conclusion']

AbstractFigureFormset = inlineformset_factory(Abstract, AbstractFigure, fields=['figure'])

class AbstractFigureForm(forms.ModelForm):
    class Meta:
        model = AbstractFigure
        fields = ['upload']


class EvaluationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop("event")
        self.abstract = kwargs.pop("abstract")
        self.user = kwargs.pop("user", None)
        super(EvaluationForm, self).__init__(*args, **kwargs)

        default_choices = [(i, i) for i in range(1, 6)]
        for criterion in Criterion.objects.filter(event=self.event):
            field_name = 'criterion_' + str(criterion.code_name)
            initial_value = None
            if self.instance.id:
                try:
                    criterion_value = CriterionValue.objects.get(evaluation=self.instance,
                                                                 criterion=criterion)
                    initial_value = criterion_value.value
                except CriterionValue.DoesNotExist:
                    pass
            
            self.fields[field_name] = forms.IntegerField(label=criterion.human_name, initial=initial_value,
                                                         widget=forms.RadioSelect, choices=default_choices,
                                                         required=True,
                                                         help_text=criterion.instructions)

    def save(self):
        # Create only if the instance has not been saved (i.e. we are
        # not editing)
        if not self.instance.id:
            evaluation = Evaluation.objects.create(abstract=self.abstract,
                                                   evaluator=self.user)
        else:
            evaluation = self.instance
            evaluation.evaluator = self.user
            evaluation.save()

        for field_name in self.cleaned_data:
            value = self.cleaned_data[field_name]
            criterion_name = field_name.replace('criterion_', '')
            criterion = Criterion.objects.get(code_name=criterion_name)
            if not self.instance.id:
                CriterionValue.objects.create(criterion=criterion,
                                              evaluation=evaluation,
                                              value=value)
            else:
                criterion_value = CriterionValue.objects.get(criterion=criterion,
                                                             evaluation=evaluation)
                criterion_value.value = value
                criterion_value.save()

        return evaluation
