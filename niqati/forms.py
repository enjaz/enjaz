# -*- coding: utf-8  -*-
"""Forms for Niqati app."""

import datetime
import autocomplete_light

from django.contrib import messages
from django.utils import timezone
from django import forms
from niqati.models import Code_Order, Code_Collection, Category, Code

class OrderForm(forms.Form):


    def __init__(self, *args, **kwargs):
        assert 'activity' in kwargs, "Kwarg 'activity' is required."
        assert 'user' in kwargs, "Kwarg 'user' is required."
        self.activity = kwargs.pop("activity", None)
        self.user = kwargs.pop("user", None)
        super(OrderForm, self).__init__(*args, **kwargs)
        episodes = self.activity.episode_set.all()
        if episodes.count() == 1:
            initial = episodes.first().pk
        else:
            initial = None
        self.fields['episode'] = forms.ModelChoiceField(episodes, label=u"الموعد", empty_label=u"اختر موعدًا ", initial=initial)
        for category in Category.objects.all():
            self.fields["count_%s" % category.pk] = forms.IntegerField(label=category.ar_label, required=False, initial=0,
                              min_value=0)
            if category.direct_entry:
                self.fields['students_%s' % category.pk] =  autocomplete_light.ModelMultipleChoiceField('NiqatiUserAutocomplete', label=u"طلاب ال" + category.ar_label, required=False)
                self.fields["count_%s" % category.pk].widget.attrs = {'data-direct-entry': 'true', 'data-category': category.pk}
            # `clean()` (below) will make sure that at least one field has a non-zero value.

    def clean(self):
        """
        Make sure that at least one category has a non-zero value.
        """
        cleaned_data = super(OrderForm, self).clean()

        # If all the values are either 0's or None's (no non-zero values), raise a validation error
        if all([(cleaned_data[field] is None or cleaned_data[field] == 0) for field in cleaned_data]):
            raise forms.ValidationError(u"أدخل، على الأقل، قيمة واحدة أكبر من الصفر.")

        # Replace None's with 0's
        for field in cleaned_data:
            if cleaned_data[field] is None:
                cleaned_data[field] = 0

        return cleaned_data

    def save(self):
        reviewing_parent = self.activity.primary_club.get_next_niqati_reviewing_parent()
        # Use this to check if we have created any collections.  If we
        # haven't (i.e. all of them are zero), don't create the order.
        collections_created = False 
        order = Code_Order.objects.create(episode=self.cleaned_data['episode'],
                                          assignee=reviewing_parent,
                                          submitter=self.user)

        # No need to keep the episode.
        del self.cleaned_data['episode']
        
        count_fields = [field_name for field_name in self.cleaned_data
                        if field_name.startswith('count')]
        for field_name in count_fields:
            category_pk = field_name.split("_")[-1]
            category = Category.objects.get(pk=int(category_pk))
            count = self.cleaned_data[field_name]
            students = self.cleaned_data.get('students_' + category_pk)
            if not count and not students: # If zero, skip
                continue
            students = self.cleaned_data.get('students_' + category_pk)
            collections_created = True # If count is 
            collection = Code_Collection.objects.create(code_count=count,
                                                        code_category=category,
                                                        parent_order=order)
            if students:
                collection.students.add(*students)
                collection.save()
        if not collections_created:
            order.delete()
            return
        else:
            return order

class RedeemCodeForm(forms.Form):
    string = forms.CharField(label="")

    def __init__(self, user, *args, **kwargs):
        super(RedeemCodeForm, self).__init__(*args, **kwargs)
        self.user = user  # Save the user as this is important for validation
        self.fields['string'].widget.attrs = {"class": "form-control input-lg input-wide english-field", "placeholder": u"أدخل رمزًا..."}

    def clean_string(self):
        """
        Check that:
        (1) code exists.
        (2) code is available.
        (3) user doesn't have another code in the same event.
        """
        # Make sure the code is uppercase, without any spaces or hyphens
        code_string = self.cleaned_data['string'].upper().replace(" ", "").replace("-", "")

        # first, check that code exists
        try:
            self.code = Code.objects.get(code_string=code_string)
        except Code.DoesNotExist:
            raise forms.ValidationError(u"هذا الرمز غير صحيح.", code="DoesNotExist")

        # next, check that code is available
        if self.code.user == self.user:
            raise forms.ValidationError(u"سبق أن استخدمت هذا الرمز", code="Used")
        elif self.code.user:
            raise forms.ValidationError(u"هذا الرمز غير متوفر.", code="Unavailable")
        else:
            # finally, check that user doesn't have another code in
            # the same episode, unless the episode allows this to
            # happen.  If they do have another code, but the new one
            # has higher point, replace it.
            if not self.code.collection.parent_order.episode.allow_multiple_niqati:
                other_codes = Code.objects.filter(collection__parent_order__episode=self.code.collection.parent_order.episode,
                                                  user=self.user)
                if other_codes.exists():
                    self.other_code = other_codes.first()
                    if self.other_code.points > self.code.points:
                        raise forms.ValidationError(u"لديك رمز آخر في نفس النشاط، وبنقاط أعلى.", code="HasOtherCode")
                    elif self.other_code.points == self.code.points:
                        raise forms.ValidationError(u"لديك رمز آخر في نفس النشاط، وبنفس مقدار النقاط.", code="HasOtherCode")
                else:
                    self.other_code = None

        return code_string

    def clean(self):
        """
        Make sure that it hasn't been two weeks since the episode ended.
        """
        cleaned_data = super(RedeemCodeForm, self).clean()
        # Check that we indeed have a valid string, and that the code
        # is part of collection
        if 'string' in cleaned_data and \
           self.code.collection and \
           timezone.now().date() > self.code.collection.parent_order.episode.end_date + datetime.timedelta(14):
            raise forms.ValidationError(u"مضى أكثر من أسبوعين على انتهاء النشاط ولم يعد ممكنا إدخال نقاطي!", code="TwoWeeks")

        return cleaned_data
    
    def process(self):
        """
        Register the submitted code for the submitting user if the submission is valid; otherwise do nothing.
        In both cases, return an appropriate message.
        :return: a tuple containing a message type and a message.
        """
        if self.is_valid():
            # If the user already has a code, count the one with more
            # points.
            if self.other_code:
                self.other_code.user = None
                self.other_code.save()
                message = u"تم إدخال الرمز القديم برمز ذي نقاط أعلى."
            else:
                message = u"تم إدخال الرمز بنجاح."
            message_level = 'success'

            new_code = Code.objects.get(code_string=self.cleaned_data['string'])
            new_code.user = self.user
            new_code.redeem_date = timezone.now()
            new_code.save()

            self.code = new_code
        else:
            message = u"حصل خطأ ما."
            message_level = 'error'

        return {'message_level': message_level, 'message': message}

