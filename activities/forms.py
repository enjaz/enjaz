# -*- coding: utf-8  -*-
"""
This module contains the forms used in the activities app.
"""
from django import forms
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import TextInput, Select
from django.forms.models import inlineformset_factory
from django.utils import timezone
from openpyxl import load_workbook

from activities.models import Activity, Episode, Review, Evaluation, Attachment, Assessment, Criterion, CriterionValue, DepositoryItem, ItemRequest
from clubs.models import Club
from core.models import StudentClubYear
from dal import autocomplete
from media.utils import can_assess_club_as_media_coordinator
import accounts.utils


class ActivityForm(ModelForm):
    """A general form, which doesn't include 'Presidency'."""
    queryset = Club.objects.current_year().visible()
    secondary_clubs = ModelMultipleChoiceField(queryset=queryset,
                                    label=Activity.secondary_clubs.field.verbose_name,
                                    help_text=Activity.secondary_clubs.field.help_text,
                                    required=False)
    episode_count = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Activity
        fields = ['name', 'category', 'description',
                  'public_description', 'goals', 'gender', 'organizers',
                  'participants', 'secondary_clubs',
                  'inside_collaborators', 'outside_collaborators',
                  'requirements']

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

        activity = super(ActivityForm, self).save(*args, **kwargs)

        # Check if any episodes have been deleted and delete them
        for episode in activity.episode_set.all():
            if episode.pk not in pk_list:
                # If the pk is not in the submitted pk's, then it has been deleted
                # by the user, so delete it from the database
                episode.delete()

        # Save the new episodes
        for episode in new_episodes:
            episode.activity = activity
            episode.save()


        return activity

class ReviewerActivityForm(ActivityForm):
    """A form which allows the submitter to choose the reviewer."""
    chosen_reviewer_club = ModelChoiceField(queryset=Club.objects.none(),
                                            required=False,
                                            label=u"المُراجع",
                                            help_text=u"الكلية المراجعة")
    class Meta:
        model = Activity
        fields = ['chosen_reviewer_club', 'name', 'category',
                  'description', 'public_description',  'goals','gender',
                  'organizers', 'participants', 'secondary_clubs',
                  'inside_collaborators', 'outside_collaborators',
                  'requirements']

class DirectActivityForm(ActivityForm):
    """A form which has 'Presidency' as an option."""
    queryset = Club.objects.current_year()
    primary_club = ModelChoiceField(queryset=queryset,
                                    label=Activity.primary_club.field.verbose_name,
                                    help_text=Activity.primary_club.field.help_text)
    secondary_clubs = ModelMultipleChoiceField(queryset=queryset,
                                    label=Activity.secondary_clubs.field.verbose_name,
                                    help_text=Activity.secondary_clubs.field.help_text,
                                    required=False)

    class Meta:
        model = Activity
        fields = ['name', 'primary_club', 'category', 'description',
                  'public_description', 'goals', 'gender', 'organizers',
                  'participants', 'secondary_clubs',
                  'inside_collaborators', 'outside_collaborators',
                  'requirements',]


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

        return cleaned_data

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['clubs_notes', 'name_notes', 'description_notes',
                  'datetime_notes', 'requirement_notes', 'goal_notes',
                  'inside_notes', 'outside_notes',
                  'organizers_notes', 'participants_notes',
                  'is_approved', 'attachment_notes',
                  'submission_date_notes']


class EvaluationForm(ModelForm):
    quality = forms.IntegerField(min_value=1, max_value=5)
    relevance = forms.IntegerField(min_value=1, max_value=5)

    def save(self, episode, user):
        evaluation = Evaluation.objects.create(episode=episode,
                                               evaluator=user,
                                               quality=self.cleaned_data['quality'],
                                               relevance=self.cleaned_data['relevance'])
        return evaluation

    class Meta:
        model = Evaluation
        fields = ['quality', 'relevance']

AttachmentFormSet = inlineformset_factory(Activity, Attachment, fields=['document', 'description'], extra=1)

class ItemRequestForm(ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['name', 'quantity']
        widgets = {'name': TextInput(attrs={'class': 'item-request-autocomplete text-right'})}

class DisabledItemRequestForm(ItemRequestForm):
    def __init__(self, *args, **kwargs):
        # Initialize the form
        super(DisabledItemRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = 'readonly'

ItemRequestFormSet = inlineformset_factory(Activity, ItemRequest, ItemRequestForm, extra=1)
DisabledItemRequestFormSet = inlineformset_factory(Activity, ItemRequest, DisabledItemRequestForm, extra=1)

class AssessmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        assert 'activity' in kwargs, "Kwarg 'activity' is required."
        assert 'user' in kwargs, "Kwarg 'user' is required."
        assert 'club' in kwargs, "Kwarg 'user' is required."
        assert 'category' in kwargs, "Kwarg 'category' is required."
        self.activity = kwargs.pop("activity", None)
        self.user = kwargs.pop("user", None)
        self.club = kwargs.pop("club", None)
        self.category = kwargs.pop("category", None)
        super(AssessmentForm, self).__init__(*args, **kwargs)

        # Only the Media Center coordinators will be able to review
        # assessments, and only in the Media Center assessment.
        if self.category == 'P' or \
           self.category == 'M' and \
           not can_assess_club_as_media_coordinator(self.user, self.activity.primary_club) and\
           not self.user.is_superuser:
            del self.fields['is_reviewed']

        if self.category == 'M':
            del self.fields['cooperator_points']

        city = accounts.utils.get_city_code(self.activity.primary_club.city)
        for criterion in Criterion.objects.filter(year=self.activity.primary_club.year,
                                                  category=self.category,
                                                  city__contains=city):
            field_name = 'criterion_' + str(criterion.code_name)
            initial_value = 0
            if self.instance.id:
                try:
                    initial_value = CriterionValue.objects.get(assessment=self.instance, criterion=criterion).value
                except CriterionValue.DoesNotExist:
                    pass
            self.fields[field_name] = forms.IntegerField(label=criterion.ar_name, initial=initial_value,
                                                                                      required=True,
                                                                                      help_text=criterion.instructions)
            if self.category == 'M':
                self.fields[field_name].widget.attrs['readonly'] = 'readonly'

    def save(self):
        notes = self.cleaned_data.pop('notes', '')
        has_shared_points = self.cleaned_data.pop('has_shared_points', False)
        cooperator_points = self.cleaned_data.pop('cooperator_points', 0)

        # If we are dealing with a Media Center assessment, check if
        # the reviewer is the presidency of the Media Center or the
        # superuser, take the input of is_reviewed.  If it is being
        # edited by a Media Center member, mark is_reviewed as false.  If the
        if self.category == 'M' \
           and (can_assess_club_as_media_coordinator(self.user, self.activity.primary_club) \
           or self.user.is_superuser):
            review_date = timezone.now()
            is_reviewed = self.cleaned_data.pop('is_reviewed', False )
        elif self.category == 'M':
            review_date = None
            is_reviewed = False
        elif self.category == 'P':
            review_date = None
            is_reviewed = True


        # Create only if the instance is not saved (i.e. we are not editing)
        if not self.instance.id:
            assessment = Assessment.objects.create(activity=self.activity,
                                                   assessor=self.user,
                                                   assessor_club=self.club,
                                                   has_shared_points=has_shared_points,
                                                   cooperator_points=cooperator_points,
                                                   notes=notes,
                                                   is_reviewed=is_reviewed,
                                                   review_date=review_date)
        else:
            assessment = self.instance
            assessment.assessor = self.user
            assessment.assessor_club = self.club
            assessment.notes = notes
            assessment.cooperator_points = cooperator_points
            assessment.is_reviewed = is_reviewed
            assessment.review_date = review_date
            assessment.has_shared_points = has_shared_points
            assessment.save()

        for field_name in self.cleaned_data:
            value = self.cleaned_data[field_name]
            criterion_name = field_name.replace('criterion_', '')
            criterion = Criterion.objects.get(code_name=criterion_name,
                                              year=self.activity.primary_club.year)

            try:
                if self.instance.id:
                    criterion_value = CriterionValue.objects.get(criterion=criterion,
                                                                 assessment=assessment)
                else:
                    raise CriterionValue.DoesNotExist
            except CriterionValue.DoesNotExist:
                print CriterionValue.objects.create(criterion=criterion,
                                                    assessment=assessment,
                                                    value=value)
            else:
                criterion_value.value = value
                criterion_value.save()

        return assessment

    class Meta:
        model = Assessment
        fields = ['notes', 'cooperator_points', 'is_reviewed', 'has_shared_points']

class UpdateDepositoryItemForm(forms.Form):
    excel_file = forms.FileField()

    def save(self):
        excel_file = self.cleaned_data['excel_file']
        wb = load_workbook(excel_file)
        categories = wb.get_sheet_names()

        DepositoryItem.objects.all().delete()
        items = []
        for category in categories:
            ws = wb[category]
            for row in ws:
                # To exclude headers and empty rows, skip all items
                # that don't have a quantity, unless the quantity is
                # explicitly not applicable (i.e. written as '-').
                if row[1].value == '-':
                    quantity = None
                else:
                    try:
                        quantity = int(row[1].value)
                    except (TypeError, ValueError, UnicodeEncodeError):
                        continue

                name = row[0].value

                # If no name, skip
                if not name:
                    continue
                else:
                    name = name.strip()
                try:
                    unit = row[2].value or ""
                except IndexError:
                    unit = ""

                if unit:
                    unit = unit.strip()

                cleaned_category = category.strip()

                item = DepositoryItem(name=name, unit=unit,
                                      quantity=quantity, category=cleaned_category)
                items.append(item)
        DepositoryItem.objects.bulk_create(items)
