# -*- coding: utf-8  -*-
from django import forms
from django.utils.translation import ugettext as _

from userena.forms import SignupForm

class SignupFormExtra(SignupForm):
    """
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.


    """
    student_id = forms.IntegerField(label=u'الرقم الجامعي')
    first_name = forms.CharField(label=_(u'الاسم الأول'),
                                max_length=30)
    last_name = forms.CharField(label=_(u'الاسم الأخير'),
                                max_length=30)

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = self.fields.keyOrder[:-3]
        new_order.insert(0, 'first_name')
        new_order.insert(1, 'last_name')
        new_order.insert(2, 'student_id')
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
        new_user.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
