from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ungettext, ugettext_lazy as _
from forms_builder.forms.models import Form, Field


class FormToBuildForm(forms.ModelForm):
    """
    A form that is used to create or edit an instance of ``forms.models.Form``.
    """
    class Meta:
        model = Form
        exclude = ('sites', 'redirect_url', 'login_required', 'send_email', 'email_from',
                   'email_copies', 'email_subject', 'email_message')


class FieldInlineFormSet(BaseInlineFormSet):
    """
    Inline formset that enforces a minimum number of non-deleted forms that are not empty.
    Enhanced version of: http://techblog.torchbox.com/post/54428118919/minimum-number-of-forms-in-a-django-formset
    """
    min_forms = 1
    min_forms_message = _("The form should contain at least 1 field")
    # min_forms_message = ungettext("The form should contain at least 1 field",
    #                               "The form should contain at least %(count)s fields",
    #                               min_forms) % {"count": min_forms}

    def clean(self):
        """
        Count the actual forms that are going to be saved and make sure they exceed the minimum.
        """
        actual_forms = 0
        for i in xrange(0, self.total_form_count()):
            form = self.forms[i]
            # Make sure form is (1) Not empty and (2) Not marked for deletion
            if not (form.instance.id is None and not form.has_changed()) \
                    and not self._should_delete_form(form):
                actual_forms += 1
        if actual_forms < self.min_forms:
            raise forms.ValidationError(self.min_forms_message)


# A form set to manage adding, modifying, or deleting fields of a form
FieldFormSet = inlineformset_factory(Form, Field, formset=FieldInlineFormSet,
                                     exclude=('slug',), extra=1, can_delete=True)