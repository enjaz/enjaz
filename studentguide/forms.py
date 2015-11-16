from django import forms

from studentguide.models import GuideProfile, Request, Report, Feedback

class GuideForm(forms.ModelForm):
    class Meta:
        model = GuideProfile
        fields = ['avatar', 'activities', 'academic_interests',
                  'nonacademic_interests', 'batch', 'tags']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['interests', 'batch']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['text']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']
