# -*- coding: utf-8  -*-
"""Forms for Niqati app."""

from django import forms
# from django.core.exceptions import ValidationError
from niqati.models import Code_Collection  #, Code

class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        assert "activity" in kwargs, "Kwarg 'activity' is required."
        activity = kwargs.pop("activity", None)
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['episode'] = forms.ModelChoiceField(activity.episode_set.all(), empty_label=u"اختر موعدًا ")
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control popover-default'
            if isinstance(self.fields[field], forms.IntegerField):
                self.fields[field].widget.attrs['data-toggle'] = 'popover'
                self.fields[field].widget.attrs['data-trigger'] = 'focus'
                self.fields[field].widget.attrs['data-placement'] = 'left'
                self.fields[field].widget.attrs['data-original-title'] = u"ملاحظة"
                self.fields[field].widget.attrs['data-content'] = u"لأفضل نتائج عند طلب كوبونات نقاطي، يرجى مراعاة ألا يزيد مجموع الكوبونات في الطلب عن ١٠٠-١٥٠ كوبون. " + \
                                                                  u"في حال كون الطلب يتجاوز ذلك، يرجى تقسيمه على أكثر من طلب."

    idea = forms.IntegerField(label=u"الفكرة", help_text=u"عدد نقاط الفكرة", required=False, initial=0,
                              min_value=0)
    organizer = forms.IntegerField(label=u"المنظمون", help_text=u"عدد نقاط التنظيم", required=False, initial=0,
                                   min_value=0)
    participant = forms.IntegerField(label=u"المشاركون", help_text=u"عدد نقاط المشاركة", required=False, initial=0,
                                     min_value=0)
    delivery_type = forms.ChoiceField(label=u"طريقة التسليم",
                                      choices=Code_Collection.DELIVERY_TYPE_CHOICES)

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
