# -*- coding: utf-8  -*-
"""Forms for Niqati app."""

from django import forms
# from django.core.exceptions import ValidationError
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
            self.fields["category_%s" % category.pk] = forms.IntegerField(label=category.ar_label, required=False, initial=0,
                              min_value=0)
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
        print "next_niqati_reviewing_parent", reviewing_parent # REMOVE
        order = Code_Order.objects.create(episode=self.cleaned_data['episode'],
                                          assignee=reviewing_parent,
                                          submitter=self.user)

        # No need to keep the episode.
        del self.cleaned_data['episode']
        
        print self.cleaned_data # REMOVE
        
        for field_name in self.cleaned_data:
            count = self.cleaned_data[field_name]
            category = Category.objects.get(pk=int(field_name.split("_")[-1]))
            if not count: # If zero, skip
                continue
            Code_Collection.objects.create(code_count=count,
                                           code_category=category,
                                           parent_order=order)

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
            code = Code.objects.get(code_string=code_string)
        except Code.DoesNotExist:
            raise forms.ValidationError(u"هذا الرمز غير صحيح.", code="DoesNotExist")

        # next, check that code is available
        if code.user == self.user:
            raise forms.ValidationError(u"سبق أن استخدمت هذا الرمز", code="Used")
        if code.user is not None:
            raise forms.ValidationError(u"هذا الرمز غير متوفر.", code="Unavailable")
        else:
            # finally, check that user doesn't have another code
            # in the same episode, unless the episode allows this
            # to happen.
            if not code.collection.parent_order.episode.allow_multiple_niqati:
                if Code.objects.filter(collection__parent_order__episode=code.collection.parent_order.episode,
                                       user=self.user).exists():
                    raise forms.ValidationError(u"لديك رمز آخر في نفس النشاط.", code="HasOtherCode")


        return code_string

    def process(self):
        """
        Register the submitted code for the submitting user if the submission is valid; otherwise do nothing.
        In both cases, return an appropriate message.
        :return: a tuple containing a message type and a message.
        """
        # TODO:
        # * If the user already has a code, count the one with more
        #   points. (Already implemented before redesign) [20150712]
        if self.is_valid():
            code = Code.objects.get(code_string=self.cleaned_data['string'])
            code.user = self.user
            code.redeem_date = timezone.now()
            code.save()

            self.code = code

            message = u"تم إدخال الرمز بنجاح."
            message_type = messages.SUCCESS

        else:
            message = u"حصل خطأ ما."
            message_type = messages.ERROR

            print self.fields['string'].errors.as_data()

        return (message_type, message)
