# -*- coding: utf-8  -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from userena.forms import SignupForm
from clubs.models import College, college_choices, section_choices

class SignupFormExtra(SignupForm):
    """
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.


    """
    first_name = forms.CharField(label=u'الاسم الأول',
                                max_length=30)
    last_name = forms.CharField(label=u'الاسم الأخير',
                                max_length=30)
    student_id = forms.IntegerField(label=u'الرقم الجامعي')
    section = forms.CharField(label=u"القسم", max_length=2, widget=forms.Select(choices=section_choices))
    college = forms.CharField(label=u"الكلية", max_length=1, widget=forms.Select(choices=college_choices))

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-6]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        new_order.insert(2, 'student_id')
        new_order.insert(3, 'section')
        new_order.insert(4, 'college')
        self.fields.keyOrder = new_order

    def clean(self):
        # Call the parent class's clean function.
        cleaned_data = super(SignupFormExtra, self).clean()

        # Remove spaces at the start and end of all text fields.
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()

        # Make sure that the email is of the university.
        if 'email' in cleaned_data and not cleaned_data['email'].endswith('ksau-hs.edu.sa'):
            email_msg = u"أدخل عنوانا جامعيا"
            self._errors['email'] = self.error_class([email_msg])
            del cleaned_data['email']

        # Make sure that the college/section choice is actually valid.
        try:
            College.objects.get(
            college_name=self.cleaned_data['college'],
            section=self.cleaned_data['section'])
        except ObjectDoesNotExist:
            college_msg = u"ليست كلية مسجلة."
            # Add an error message to specific fields.
            self._errors['college'] = self.error_class([college_msg])
            self._errors['section'] = self.error_class([college_msg])
            # Remove invalid fields
            del cleaned_data['college']
            del cleaned_data['section']

        return cleaned_data

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        # Add default permissions
        add_book = Permission.objects.get(codename='add_book')
        add_bookrequest = Permission.objects.get(codename='add_bookrequest')
        new_user.user_permissions.add(add_book, add_bookrequest)
        new_user.save()

        # Append the extra fields
        user_profile = new_user.get_profile()
        user_profile.first_name = self.cleaned_data['first_name']
        user_profile.last_name = self.cleaned_data['last_name']
        user_profile.student_id = self.cleaned_data['student_id']
        user_college = College.objects.get(
            college_name=self.cleaned_data['college'],
            section=self.cleaned_data['section'])

        user_profile.college = user_college
        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
