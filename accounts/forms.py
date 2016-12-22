# -*- coding: utf-8  -*-
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from accounts.models import CommonProfile
from bulb.models import Point
from clubs.models import College, city_choices, college_choices, section_choices, gender_choices
from core.models import StudentClubYear
import core.utils
from userena.forms import SignupForm


class EnjazSignupForm(SignupForm):
    # FIXME: Dirty 'verbose_name' hack?
    ar_first_name = forms.CharField(label=CommonProfile._meta.get_field('ar_first_name').verbose_name,
                                max_length=30)
    ar_middle_name = forms.CharField(label=CommonProfile._meta.get_field('ar_middle_name').verbose_name,
                                max_length=30)
    ar_last_name = forms.CharField(label=CommonProfile._meta.get_field('ar_last_name').verbose_name,
                                max_length=30)
    en_first_name = forms.CharField(label=CommonProfile._meta.get_field('en_first_name').verbose_name,
                                max_length=30)
    en_middle_name = forms.CharField(label=CommonProfile._meta.get_field('en_middle_name').verbose_name,
                                max_length=30)
    en_last_name = forms.CharField(label=CommonProfile._meta.get_field('en_last_name').verbose_name,
                                max_length=30)
    en_last_name = forms.CharField(label=CommonProfile._meta.get_field('en_last_name').verbose_name,
                                max_length=30)

    def clean(self):
        # Call the parent class's clean function.
        cleaned_data = super(EnjazSignupForm, self).clean()

        # Remove spaces at the start and end of all text fields.
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()

        # Make sure that the mobile numbers contain only digits and
        # pluses:
        if 'mobile_number' in cleaned_data:
            mobile_number_msg = ""
            cleaned_data['mobile_number'] = core.utils.hindi_to_arabic(cleaned_data['mobile_number'])
            if len(cleaned_data['mobile_number']) < 10:
                mobile_number_msg = u"الرقم الذي أدخلت ناقص"
            if not all([number in '1234567890+' for number in cleaned_data['mobile_number']]):
                mobile_number_msg = u"أدخل أرقاما فقط"
            if mobile_number_msg:
                self._errors['mobile_number'] = self.error_class([mobile_number_msg])
                del cleaned_data['mobile_number']

        return cleaned_data


class StudentSignupForm(EnjazSignupForm):
    """
    A form that includes extra student-related fields.
    """
    student_id = forms.IntegerField(label=CommonProfile._meta.get_field('student_id').verbose_name, required=False)
    # Since the mobile number starts with a zero, store it as a
    # string.
    mobile_number = forms.CharField(label=CommonProfile._meta.get_field('mobile_number').verbose_name)
    section = forms.CharField(label=u"القسم", max_length=2, widget=forms.Select(choices=section_choices), required=False)
    college = forms.CharField(label=CommonProfile._meta.get_field('college').verbose_name, max_length=1, widget=forms.Select(choices=college_choices))
    gender = forms.CharField(label=u"الجنس", max_length=1, widget=forms.Select(choices=gender_choices))
    badge_number = forms.IntegerField(label=CommonProfile._meta.get_field('badge_number').verbose_name, required=False)
    city = forms.CharField(label=u"المدينة", max_length=1, widget=forms.Select(choices=city_choices))
    alternative_email = forms.EmailField(label=CommonProfile._meta.get_field('alternative_email').verbose_name)

    def __init__(self, *args, **kw):
        super(StudentSignupForm, self).__init__(*args, **kw)
        # We don't want usernames (We could have inherited userena's
        # SignupFormOnlyEmail, but it's more tricky to modify.)
        del self.fields['username']

    def clean(self):
        # Call the parent class's clean function.
        cleaned_data = super(StudentSignupForm, self).clean()


        # Make sure that the email is of the university or the hospital.
        if 'email' in cleaned_data and not \
           cleaned_data['email'].endswith('ksau-hs.edu.sa') and \
           not cleaned_data['email'].endswith('ngha.med.sa'):
            email_msg = u"أدخل عنوانا جامعيا"
            self._errors['email'] = self.error_class([email_msg])
            del cleaned_data['email']


        # Since Jeddah and Al-Hasa have only one campus, the section
        # equals the city.
        if 'city' in cleaned_data and \
           cleaned_data['city'] in ['J', 'A']:
            cleaned_data['section'] = cleaned_data['city']


        # Make sure that the college/section choice is actually valid.
        try:
            self.college = College.objects.get(
                name=cleaned_data['college'],
                city=cleaned_data['city'],
                section=cleaned_data['section'],
                gender=cleaned_data['gender'])
        except College.DoesNotExist:
            college_msg = u"ليست كلية مسجلة."
            # Add an error message to specific fields.
            self._errors['college'] = self.error_class([college_msg])
            self._errors['section'] = self.error_class([college_msg])
            self._errors['gender'] = self.error_class([college_msg])
            # Remove invalid fields
            del cleaned_data['college']
            del cleaned_data['section']
            del cleaned_data['gender']

        return cleaned_data

    def save(self):
        # Save the parent form and get the user
        new_user = super(StudentSignupForm, self).save()

        self.cleaned_data['email'] = self.cleaned_data['email'].lower()
        self.cleaned_data['username'] = self.cleaned_data['email'].split('@')[0]
        self.cleaned_data['username'] = self.cleaned_data['username']

        # Add initial Bulb balance.
        current_year = StudentClubYear.objects.get_current()
        Point.objects.create(year=current_year,
                             user=new_user,
                             note=u"رصيد مبدئي.",
                             value=1,
                             category='L')
        Point.objects.create(year=current_year,
                             user=new_user,
                             note=u"رصيد مبدئي.",
                             value=1,
                             category='G')

        CommonProfile.objects.create(user=new_user,
                                     is_student=True,
                                     profile_type="S",
                                     ar_first_name=self.cleaned_data['ar_first_name'],
                                     ar_middle_name=self.cleaned_data['ar_middle_name'],
                                     ar_last_name=self.cleaned_data['ar_last_name'],
                                     en_first_name=self.cleaned_data['en_first_name'],
                                     en_middle_name=self.cleaned_data['en_middle_name'],
                                     en_last_name=self.cleaned_data['en_last_name'],
                                     alternative_email=self.cleaned_data['alternative_email'],
                                     badge_number=self.cleaned_data.get('badge_number'),
                                     city=self.cleaned_data['city'],
                                     mobile_number=self.cleaned_data['mobile_number'],
                                     student_id=self.cleaned_data.get('student_id'),
                                     college=self.college,
                                     job_description="",
                                     college_name="",
                                     nonuser_city="",
                                    )

        return new_user

class NonStudentSignupForm(EnjazSignupForm):
    """
    A form that includes extra non-student-related fields.
    """
    # Since the mobile number starts with a zero, store it as a
    # string.  For non-students, this field is going to be optional.
    mobile_number = forms.CharField(label=CommonProfile._meta.get_field('mobile_number').verbose_name,
                                    required=False)
    job_description = forms.CharField(label=CommonProfile._meta.get_field('job_description').verbose_name,
                                       max_length=50)
    badge_number = forms.IntegerField(label=CommonProfile._meta.get_field('badge_number').verbose_name, required=False)
    city = forms.CharField(label=u"المدينة", max_length=1, widget=forms.Select(choices=city_choices))
    alternative_email = forms.EmailField(label=CommonProfile._meta.get_field('alternative_email').verbose_name)

    def __init__(self, *args, **kw):
        super(NonStudentSignupForm, self).__init__(*args, **kw)
        # We don't want usernames (We could have inherited userena's
        # SignupFormOnlyEmail, but it's more tricky to modify.)
        del self.fields['username']

    def clean(self):

        # Call the parent class's clean function.
        cleaned_data = super(NonStudentSignupForm, self).clean()


        # Make sure that the email is of the university or the hospital.
        if 'email' in cleaned_data and not \
           cleaned_data['email'].endswith('ksau-hs.edu.sa') and \
           not cleaned_data['email'].endswith('ngha.med.sa'):
            email_msg = u"أدخل عنوانا جامعيا"
            self._errors['email'] = self.error_class([email_msg])
            del cleaned_data['email']

        return cleaned_data

    def save(self):
        # Save the parent form and get the user
        new_user = super(NonStudentSignupForm, self).save()

        self.cleaned_data['username'] = self.cleaned_data['email'].split('@')[0]
        self.cleaned_data['username'] = self.cleaned_data['username']

        mobile_number = self.cleaned_data.get('mobile_number', '')
        CommonProfile.objects.create(user=new_user,
                                     is_student=False,
                                     profile_type="E",
                                     ar_first_name=self.cleaned_data['ar_first_name'],
                                     ar_middle_name=self.cleaned_data['ar_middle_name'],
                                     ar_last_name=self.cleaned_data['ar_last_name'],
                                     en_first_name=self.cleaned_data['en_first_name'],
                                     en_middle_name=self.cleaned_data['en_middle_name'],
                                     en_last_name=self.cleaned_data['en_last_name'],
                                     alternative_email=self.cleaned_data['alternative_email'],
                                     badge_number=self.cleaned_data['badge_number'],
                                     city=self.cleaned_data['city'],
                                     mobile_number=mobile_number,
                                     job_description=self.cleaned_data['job_description'],
                                     college=None,
                                     student_id=None,
                                     college_name="",
                                     nonuser_city="",
                                     )
        return new_user

class NonUserSignupForm  (EnjazSignupForm):
    mobile_number = forms.CharField(label=CommonProfile._meta.get_field('mobile_number').verbose_name,
                                    required=False)
    college_name = forms.CharField(label=CommonProfile._meta.get_field('college_name').verbose_name,
                                max_length=30, required=False)
    nonuser_city = forms.CharField(label=CommonProfile._meta.get_field('nonuser_city').verbose_name,
                                max_length=30, required=False)
    gender = forms.CharField(label=u"الجنس", max_length=1, widget=forms.Select(choices=gender_choices))

    def clean (self):

        # Call the parent class's clean function.
        cleaned_data = super(NonUserSignupForm, self).clean()

        #  Make sure that the email is not of the university or the hospital.
        if 'email' in cleaned_data and \
           cleaned_data['email'].endswith('ksau-hs.edu.sa') and \
           cleaned_data['email'].endswith('ngha.med.sa'):
                email_msg = u"استخدم النموذج المُخصص"
                self._errors['email'] = self.error_class([email_msg])
                del cleaned_data['email']

        return cleaned_data

    def save(self):
        # Save the parent form and get the user
        new_user = super(NonUserSignupForm, self).save()

        mobile_number = self.cleaned_data.get('mobile_number', '')

        CommonProfile.objects.create(user=new_user,
                                     is_student=False,
                                     profile_type="N",
                                     ar_first_name=self.cleaned_data['ar_first_name'],
                                     ar_middle_name=self.cleaned_data['ar_middle_name'],
                                     ar_last_name=self.cleaned_data['ar_last_name'],
                                     en_first_name=self.cleaned_data['en_first_name'],
                                     en_middle_name=self.cleaned_data['en_middle_name'],
                                     en_last_name=self.cleaned_data['en_last_name'],
                                     alternative_email="",
                                     badge_number="",
                                     mobile_number=self.cleaned_data['mobile_number'],
                                     job_description="",
                                     city=None,
                                     student_id=None,
                                     college=None,
                                     college_name=self.cleaned_data['college_name'],
                                     nonuser_city=self.cleaned_data['nonuser_city'],
                                    )
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
                                     label=u'تذكرني (مدّة شهر)')


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
        # Make sure that the email is of the university or the hospital.

        if 'email' in cleaned_data and not \
           cleaned_data['email'].endswith('ksau-hs.edu.sa') and \
           not cleaned_data['email'].endswith('ngha.med.sa'):
            email_msg = u"أدخل عنوانا جامعيا"
            self._errors['email'] = self.error_class([email_msg])
            del cleaned_data['email']

class EditStudentCommonProfile(forms.ModelForm):
    section = forms.CharField(label=u"القسم", max_length=2, widget=forms.Select(choices=section_choices), required=False)
    college = forms.CharField(label=CommonProfile._meta.get_field('college').verbose_name, max_length=1, widget=forms.Select(choices=college_choices))
    gender = forms.CharField(label=u"الجنس", max_length=1, widget=forms.Select(choices=gender_choices))

    class Meta:
        model = CommonProfile
        fields = ['ar_first_name', 'ar_middle_name', 'ar_last_name',
                  'en_first_name', 'en_middle_name', 'en_last_name',
                  'alternative_email', 'student_id', 'badge_number',
                  'mobile_number', 'city']

    def clean(self):
        cleaned_data = super(EditStudentCommonProfile, self).clean()
        # Since Jeddah and Al-Hasa have only one campus, the section
        # equals the city.
        if 'city' in cleaned_data and \
           cleaned_data['city'] in ['J', 'A']:
            cleaned_data['section'] = cleaned_data['city']

        # Make sure that the college/section choice is actually valid.
        try:
            print cleaned_data['college'], cleaned_data['city'], cleaned_data['section'], cleaned_data['gender']
            self.college = College.objects.get(
                name=cleaned_data['college'],
                city=cleaned_data['city'],
                section=cleaned_data['section'],
                gender=cleaned_data['gender'])
        except College.DoesNotExist:
            college_msg = u"ليست كلية مسجلة."
            # Add an error message to specific fields.
            self._errors['college'] = self.error_class([college_msg])
            self._errors['section'] = self.error_class([college_msg])
            self._errors['gender'] = self.error_class([college_msg])
            # Remove invalid fields
            del cleaned_data['college']
            del cleaned_data['section']
            del cleaned_data['gender']

        return cleaned_data

    def save(self):
        common_profile = super(EditStudentCommonProfile, self).save()
        common_profile.college = self.college
        common_profile.save()

class ResendForm(forms.Form):
    email = forms.EmailField()
