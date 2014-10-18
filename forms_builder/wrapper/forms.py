from django import forms
from django.forms.models import inlineformset_factory
from forms_builder.forms.models import Form, Field


class FormToBuildForm(forms.ModelForm):
    """
    A form that is used to create or edit an instance of ``forms.models.Form``.
    """
    class Meta:
        model = Form
        exclude = ('sites', 'redirect_url', 'login_required', 'send_email', 'email_from',
                   'email_copies', 'email_subject', 'email_message')

# A form set to manage adding, modifying, or deleting fields of a form
FieldFormSet = inlineformset_factory(Form, Field, exclude=('slug',), extra=1, can_delete=True)