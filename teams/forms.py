from django.forms import ModelForm
from .models import Teams


class TeamForm(ModelForm):
    class Meta:
        model = Teams
        fields = ['ar_name','en_name','description', 'email',
                  'parent', 'coordinator', 'city', 'gender',
                  'category', 'logo', 'is_visible']
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(TeamForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data


class DisabledTeamForm(TeamForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['description']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledTeamForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited).
        if self.instance:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super(DisabledTeamForm, self).clean()
        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data

class AddTeamMembersForm(ModelForm):
    class Meta:
        model = Teams
        fields = ['members']