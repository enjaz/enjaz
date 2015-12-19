# -*- coding: utf-8  -*-
from django import forms

from hpc.models import Abstract, Evaluation

default_choices = [(i, i) for i in range(1, 6)]

class AbstractForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ['title', 'authors', 'university', 'college',
                  'presenting_author', 'email', 'phone', 'level',
                  'presentation_preference', 'attachment']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['clear_objectives', 'informative_abstract',
                  'introduction', 'clear_method', 'good_statistics',
                  'clear_sampling', 'clear_results',
                  'clear_discussion', 'good_english',
                  'overall_evaluation']
        widgets = {field: forms.RadioSelect for field in fields}

