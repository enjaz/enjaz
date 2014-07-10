# -*- coding: utf-8  -*-
from django import forms
from django.forms import ModelForm

from media.models import FollowUpReport

class FollowUpReportForm(ModelForm):
    class Meta:
        model = FollowUpReport
        fields = ['description', 'start_date', 'end_date',
                  'start_time', 'end_time', 'location',
                  'organizer_count', 'participant_count']