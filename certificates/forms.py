# -*- coding: utf-8  -*-
from activities.models import Episode
from certificates.models import Certificate, CertificateTemplate, CertificateRequest, TextPosition
from certificates import utils
from dal import autocomplete
from django import forms
from django.forms import  inlineformset_factory
import clubs.utils


class CertificateRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CertificateRequestForm, self).__init__(*args, **kwargs)

        if clubs.utils.is_coordinator_or_deputy_of_any_club(self.user):
            user_clubs = clubs.utils.get_user_coordination_and_deputyships(self.user)
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
        fields = ['episode', 'description', 'text', 'user_list',
                  'users']
        widgets = {'users':
                   autocomplete.ModelSelect2Multiple(url='user-autocomplete',
                                                     attrs={ 'data-placeholder': 'أَضف اسمًا',
                                                             'data-html': 'true', })}

class CertificateTemplateForm(forms.ModelForm):
    example_text =  forms.CharField(label=u"المثال", initial="Nada Abdullah")
    is_approved = forms.BooleanField(label=u"معتمد؟")

    def save(self):
        template = super(CertificateTemplateForm, self).save()
        if self.cleaned_data['is_approved']:
            certificate_request = template.certificate_request
            certificate_request.is_approved = True
            certificate_request.save()
            for user in template.certificate_request.users.all():
                certificate = template.generate_certificate(user, user.common_profile.get_en_full_name())

        return template

    class Meta:
        model = CertificateTemplate
        fields = ['example_text', 'description', 'image',
                  'image_format']

class VerifyCertificateForm(forms.Form):
    verification_code = forms.CharField(max_length=6, min_length=6,
                                        label=u"رمز التحقق")

PositionFormset =  inlineformset_factory(CertificateTemplate, TextPosition,
                                         fields=('y_position', 'y_center',
                                                 'x_position','x_center',
                                                 'font_family',
                                                 'size', 'color'),
                                         widgets={'color': forms.TextInput(attrs={'class': 'jscolor english-field'})})




class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('__all__')
        widgets = {
            'user': autocomplete.ModelSelect2(url='user-autocomplete', attrs={'data-html': 'true'})
        }
