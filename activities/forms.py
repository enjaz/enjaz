# -*- coding: utf-8  -*-
"""
This module contains the forms used in the activities app.
"""
from django import forms
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import TextInput

from clubs.models import Club
from activities.models import Activity, Episode, Review, Evaluation


class ActivityForm(ModelForm):
    """A general form, which doesn't include 'Presidency'."""
    queryset = Club.objects.exclude(english_name="Presidency")
    primary_club = ModelChoiceField(queryset=queryset,
                                    label=Activity.primary_club.field.verbose_name,
                                    help_text=Activity.primary_club.field.help_text)
    secondary_clubs = ModelMultipleChoiceField(queryset=queryset,
                                    label=Activity.secondary_clubs.field.verbose_name,
                                    help_text=Activity.secondary_clubs.field.help_text,
                                    required=False)
    episode_count = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Activity
        fields = ['primary_club', # TODO: primary club is already known (signed in):
                                  # no need to include as field
                  'name', 'category', 'description', 'public_description',
                  'organizers', 'participants',
                  'secondary_clubs', 'inside_collaborators',
                  'outside_collaborators', 'requirements',
                  'collect_participants', 'participant_colleges']

    def __init__(self, *args, **kwargs):
        """
        Dynamically add date, time and location fields based on how many
        Episodes are added in the original form. The number of episodes is
        included as a hidden field with the name episode_count.
        Based on this StackOverflow thread:
        http://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form
        """
        # If an instance is passed, then store it in the instance variable.
        # This will be used in populating the episode fields when an instance
        # is passed.
        instance = kwargs.get('instance', None)
                
        # Initialize the form
        super(ActivityForm, self).__init__(*args, **kwargs)

        # Determine how many episodes there are:
        episode_count = 1 # default value
        # First check if an instance is passed. If true, then get the episode count of that instance
        if instance: episode_count = instance.episode_set.count()
        
        # If data is passed (whether it's for a new activity or editing),
        # set episode_count to the episode count within the data.
        # This may override the value obtained from the instance if there is an update in the episodes
        if self['episode_count'].value(): episode_count = self['episode_count'].value()
        
        # In any case, the episode count should be at least 1
        if episode_count < 1: episode_count = 1
        
        #  Set the value of the hidden field to the episode count
        self.fields['episode_count'].initial = episode_count
        
        # If an instance is passed and is saved (has a pk), load its episodes
        if instance and instance.pk:
            instance_episodes = instance.episode_set.all()
        
        # Now add the custom date, time and location fields
        for i in range(int(episode_count)):
            # The disability status is the opposite of is_editable
            self.fields['episode_pk{i}'.format(i=i)] = forms.CharField(widget=forms.HiddenInput(), required=False)
            self.fields['start_date{i}'.format(i=i)] = forms.DateField(label='تاريخ البداية')
            self.fields['end_date{i}'.format(i=i)] = forms.DateField(label='تاريخ النهاية')
            self.fields['start_time{i}'.format(i=i)] = forms.TimeField(label='وقت البداية')
            self.fields['end_time{i}'.format(i=i)] = forms.TimeField(label='وقت النهاية')
            self.fields['location{i}'.format(i=i)] = forms.CharField(max_length=128, label='المكان')
            
            # If an instance exists (has a pk), then load the fields
            # with the instance episode values.  An IndexError arises
            # when submitting an edit form in which new episodes have
            # been added, since episode_count will increase beyond the
            # lenght of instance_episodes.  In this case just leave
            # the new fields empty as they will be filled by the
            # submitted data.
            if instance and instance.pk:
                try:
                    self.fields['episode_pk{i}'.format(i=i)].initial = instance_episodes[i].pk
                    self.fields['start_date{i}'.format(i=i)].initial = instance_episodes[i].start_date
                    self.fields['end_date{i}'.format(i=i)].initial = instance_episodes[i].end_date
                    self.fields['start_time{i}'.format(i=i)].initial = instance_episodes[i].start_time
                    self.fields['end_time{i}'.format(i=i)].initial = instance_episodes[i].end_time
                    self.fields['location{i}'.format(i=i)].initial = instance_episodes[i].location
                except IndexError:
                    pass

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        # Remove spaces at the start and end of all text fields.
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()                
        # TODO: Check if end_date is after start_date

        return cleaned_data
    
    def save(self, *args, **kwargs):
        # Extract and save the episodes, perform a normal save,
        # and link the episodes to the activity
        
        # First, check how many episodes we have
        episode_count = self.cleaned_data['episode_count']
        new_episodes = []
        pk_list = [] # A list for storing any pk's submitted through the form
                     # Comparing this list to the list of episode pk's from the
                     # the database will tell us which episodes, if any, have
                     # been deleted 
        
        for i in range(int(episode_count)):
            # Get the details of each episode and store them in an Episode object
            pk = self.cleaned_data.pop('episode_pk{i}'.format(i=i), None)
            start_date = self.cleaned_data.pop('start_date{i}'.format(i=i))
            end_date = self.cleaned_data.pop('end_date{i}'.format(i=i))
            start_time = self.cleaned_data.pop('start_time{i}'.format(i=i))
            end_time = self.cleaned_data.pop('end_time{i}'.format(i=i))
            location = self.cleaned_data.pop('location{i}'.format(i=i))
            
            # If there is a pk, i.e. the episode already exists in the database, just update it
            # Otherwise create a new one
            if pk:
                pk_list.append(int(pk))
                episode = Episode.objects.get(pk=pk)
                
                episode.start_date = start_date
                episode.end_date = end_date
                episode.start_time = start_time
                episode.end_time = end_time
                episode.location = location
                
                episode.save()
            else:
                episode = Episode(start_date=start_date,
                                  end_date=end_date,
                                  start_time=start_time,
                                  end_time=end_time,
                                  location=location)
                new_episodes.append(episode)

        print "PK list: ", pk_list

        activity = super(ActivityForm, self).save(*args, **kwargs)
        
        # Check if any episodes have been deleted and delete them
        for episode in activity.episode_set.all():
            print "PK: ", episode.pk, " is in list: " if episode.pk in pk_list else " is not in list: ", pk_list
            if episode.pk not in pk_list:
                # If the pk is not in the submitted pk's, then it has been deleted
                # by the user, so delete it from the database
                episode.delete()
        
        # Save the new episodes
        for episode in new_episodes:
            episode.activity = activity
            episode.save()

            
        return activity            
    
class DirectActivityForm(ActivityForm):
    """A form which has 'Presidency' as an option."""
    queryset = Club.objects.all()
    primary_club = ModelChoiceField(queryset=queryset,
                                    label=Activity.primary_club.field.verbose_name,
                                    help_text=Activity.primary_club.field.help_text)
    secondary_clubs = ModelMultipleChoiceField(queryset=queryset,
                                    label=Activity.secondary_clubs.field.verbose_name,
                                    help_text=Activity.secondary_clubs.field.help_text,
                                    required=False)

class DisabledActivityForm(ActivityForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['public_description']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledActivityForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited) and is_editable is False, so you can disable most
        # fields.
        if self.instance and not self.instance.is_editable:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        # m2m need a special workaround.
        m2m_fields = ['secondary_clubs', 'participant_colleges']

        cleaned_data = super(DisabledActivityForm, self).clean()

        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    try:
                        if field in m2m_fields:
                            cleaned_data[field] = getattr(self.instance, field).all()
                        else:
                            cleaned_data[field] = getattr(self.instance, field)
                    except AttributeError: # For episode fields
                        pass
        else:
            print "No instance!"

        return cleaned_data

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['clubs_notes', 'name_notes', 'description_notes',
                  'datetime_notes', 'requirement_notes',
                  'inside_notes', 'outside_notes',
                  'organizers_notes', 'participants_notes',
                  'is_approved', 'submission_date_notes']


class EvaluationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = TextInput()
            self.fields[field].widget.attrs = {'class': 'knob', 'data-min': 0, 'data-max': 5,
                                               'data-width': 125, 'data-height': 125, 'data-thickness': .25,
                                               'data-fgcolor': '#00b19d', 'data-bgcolor': '#ebebeb',
                                               'data-anglearc': 240, 'data-angleoffset': -120}
    quality = forms.IntegerField(min_value=1, max_value=5)
    relevance = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Evaluation
        fields = ['quality', 'relevance']
