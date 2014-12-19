from django.forms import ModelForm
from clubs.models import Club


class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['name','english_name','description', 'email',
                  'parent', 'coordinator']
    def clean(self):
        # Remove spaces at the start and end of all text fields.
        cleaned_data = super(ClubForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()
        return cleaned_data


class DisabledClubForm(ClubForm):
    def __init__(self, *args, **kwargs):
        # Fields to keep enabled.
        self.enabled_fields = ['description']
        # If an instance is passed, then store it in the instance variable.
        # This will be used to disable the fields.
        self.instance = kwargs.get('instance', None)

        # Initialize the form
        super(DisabledClubForm, self).__init__(*args, **kwargs)

        # Make sure that an instance is passed (i.e. the form is being
        # edited).
        if self.instance:
            for field in self.fields:
                if not field in self.enabled_fields:
                    self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        cleaned_data = super(DisabledClubForm, self).clean()
        if self.instance:
            for field in cleaned_data:
                if not field in self.enabled_fields:
                    cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data


class ModifyClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ['description', 'email',
                  'parent', 'coordinator']