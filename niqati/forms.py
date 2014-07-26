# -*- coding: utf-8  -*-
"""Forms for Niqati app."""

from django import forms
from niqati.models import Code_Collection


class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    idea = forms.IntegerField(label=u"الفكرة", help_text=u"عدد نقاط الفكرة", required=False, initial=0,
                              min_value=0)
    organizer = forms.IntegerField(label=u"المنظمون", help_text=u"عدد نقاط التنظيم", required=False, initial=0,
                                   min_value=0)
    participant = forms.IntegerField(label=u"المشاركون", help_text=u"عدد نقاط المشاركة", required=False, initial=0,
                                     min_value=0)
    delivery_type = forms.ChoiceField(label=u"طريقة التسليم",
                                      choices=Code_Collection.DELIVERY_TYPE_CHOICES)