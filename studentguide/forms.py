from django import forms

from studentguide.models import GuideProfile, Request, Report, Feedback, MentorOfTheMonth

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
        fields = ['session_date', 'session_location',
                  'session_duration', 'means_of_communication',
                  'points_discussed', 'plans_suggested',
                  'issues_faced', 'other_comments', 'next_session_date']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']
