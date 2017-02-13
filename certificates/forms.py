# -*- coding: utf-8  -*-
from activities.models import Episode
from certificates.models import CertificateTemplate, CertificateRequest
from dal import autocomplete
from django import forms
import clubs.utils


class CertificateRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CertificateRequestForm, self).__init__(*args, **kwargs)

        if clubs.utils.is_coordinator_or_deputy_of_any_club(self.user):
            user_clubs = get_user_coordination_and_deputyships(self.user)
            self.club = user_clubs.first()
            episodes = Episode.objects.filter(activity__primary_club__in=user_clubs)
            self.fields['episode'] = forms.ModelChoiceField(episodes,
                                                            label=u"الموعد", empty_label=u"اختر موعدًا ",
                                                            required=False)
        else:
            self.club = None
            del self.fields['episode']
    def save(self, *args, **kwargs):
        certificate_request = super(CertificateRequestForm, self).save(commit=False)
        certificate_request.submitter_club = self.club
        certificate_request.save()
        return certificate_request

    class Meta:
        model = CertificateRequest
        fields = ['episode', 'description', 'text', 'student_list',
                  'students']
        widgets = {'students':
                   autocomplete.ModelSelect2Multiple(url='bulb:bulb-user-autocomplete',
                                                     attrs={ 'data-placeholder': 'أَضف اسمًا',
                                                             'data-html': 'true', })}

class CertificateTemplateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CertificateTemplateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required=False

    example_text =  forms.CharField(label=u"المثال", initial="Nada Abdullah")
    is_approved = forms.NullBooleanField(label="معتمد؟")
    class Meta:
        model = CertificateTemplate
        fields = ['example_text', 'description', 'color', 'font_size',
                  'x_position', 'y_position', 'image', 'image_format']
        widgets = {'color': forms.TextInput(attrs={'class': 'jscolor english-field'}),
                   'x_position': forms.HiddenInput(),
                   'y_position': forms.HiddenInput()}


class VerifyCertificateForm(forms.Form):
    verification_code = forms.CharField(max_length=6, min_length=6,
                                        label=u"رمز التحقق")
