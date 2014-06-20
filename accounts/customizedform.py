# -*- coding: utf-8  -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from userena.forms import SignupForm
from clubs.models import College, college_choices, section_choices

class SignupFormExtra(SignupForm):
    """
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.


    """
    ar_first_name = forms.CharField(label=u'الاسم الأول',
                                max_length=30)
    ar_middle_name = forms.CharField(label=u'الاسم الأوسط',
                                max_length=30)
    ar_last_name = forms.CharField(label=u'الاسم الأخير',
                                max_length=30)
    en_first_name = forms.CharField(label=u'الاسم الأول',
                                max_length=30)
    en_middle_name = forms.CharField(label=u'الاسم الأوسط',
                                max_length=30)
    en_last_name = forms.CharField(label=u'الاسم الأخير',
                                max_length=30)
    badge_number = forms.IntegerField(label=u'رقم البطاقة')
    student_id = forms.IntegerField(label=u'الرقم الجامعي')
    # Since it starts with a zero, store it as a string.
    mobile_number = forms.CharField(label=u'رقم الجوال')
    section = forms.CharField(label=u"القسم", max_length=2, widget=forms.Select(choices=section_choices))
    college = forms.CharField(label=u"الكلية", max_length=1, widget=forms.Select(choices=college_choices))

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupFormExtra, self).__init__(*args, **kw)
        # We don't want usernames (We could have inherited userena's
        # SignupFormOnlyEmail, but it's more tricky to modify.)
        del self.fields['username']

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

        # Make sure that the mobile numbers contain only digits and
        # pluses:
        if 'mobile_number' in cleaned_data:
            mobile_number_msg = ""
            if len(cleaned_data['mobile_number']) < 10:
                mobile_number_msg = u"الرقم الذي أدخلت ناقص"
            for char in cleaned_data['mobile_number']:
                if not char in '1234567890+':
                    mobile_number_msg = u"أدخل أرقاما فقط"
                    break
            if mobile_number_msg:
                self._errors['mobile_number'] = self.error_class([mobile_number_msg])
                del cleaned_data['mobile_number']

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

        self.cleaned_data['username'] = self.cleaned_data['email'].split('@')[0]
        # All username names should be lower-case.
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        # Save the parent form and get the user
        new_user = super(SignupFormExtra, self).save()

        # Add default permissions
        add_book = Permission.objects.get(codename='add_book')
        add_bookrequest = Permission.objects.get(codename='add_bookrequest')
        submit_niqati_code = Permission.objects.get(codename='submit_code')
        view_niqati_report = Permission.objects.get(codename='view_student_report')
        new_user.user_permissions.add(add_book, add_bookrequest, submit_niqati_code, view_niqati_report)
        new_user.save()

        # Append the extra fields
        user_profile = new_user.get_profile()
        user_profile.ar_first_name = self.cleaned_data['ar_first_name']
        user_profile.ar_middle_name = self.cleaned_data['ar_middle_name']
        user_profile.ar_last_name = self.cleaned_data['ar_last_name']
        user_profile.en_first_name = self.cleaned_data['en_first_name']
        user_profile.en_middle_name = self.cleaned_data['en_middle_name']
        user_profile.en_last_name = self.cleaned_data['en_last_name']
        user_profile.badge_number = self.cleaned_data['badge_number']
        user_profile.student_id = self.cleaned_data['student_id']
        user_profile.mobile_number = self.cleaned_data['mobile_number']
        user_college = College.objects.get(
            college_name=self.cleaned_data['college'],
            section=self.cleaned_data['section'])

        user_profile.college = user_college
        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user


class ModifiedAuthenticationForm(forms.Form):
    identification = forms.CharField(label=u"البريد",
                                        widget=forms.TextInput(attrs={'class': 'required'}),
                                        max_length=75,
                                        error_messages={'required': u"رجاءً أدخل بريدك الجامعي."})
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs={'class': 'required'}, render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),
                                     required=False,
                                     label=u'تذكرني شهرا')
    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            if '@' in identification:
                username = identification.split('@')[0]
            else:
                username = identification

            # All usernames should alwyas be lower-case and with no
            # spaces. This will make life easier.
            username = username.lower().strip()


            # The final username should be returned to userena to
            # process.
            self.cleaned_data['identification'] = username

            user = authenticate(username=username, password=password)
            if not user is None:
                return self.cleaned_data

        raise forms.ValidationError(_(u"الرجاء إدخال عنوان بريد وكلمة سر صحيحين."))
