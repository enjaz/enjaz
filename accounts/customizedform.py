# -*- coding: utf-8  -*-
from django import forms
from django.utils.translation import ugettext as _

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
    section = forms.CharField(label=u"القسم", max_length=1, widget=forms.Select(choices=section_choices))
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

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        # First save the parent form and get the user.
        new_user = super(SignupFormExtra, self).save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.student_id = self.cleaned_data['student_id']
        user_college = College.objects.get(
            college_name=self.cleaned_data['college'],
            section=self.cleaned_data['section'])
        new_user.college = user_college
        new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
