# -*- coding: utf-8  -*-
"""Forms for Niqati app."""

from django import forms
# from django.core.exceptions import ValidationError
from niqati.models import Code_Collection  #, Code

class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
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

# # TODO: use django forms in code submission
# class SubmissionForm(forms.ModelForm):
#     """
#     A form that handles code submission.
#     """
#     def __init__(self, *args, **kwargs):
#         super(SubmissionForm, self).__init__(*args, **kwargs)
#         self.user = self.instance.user
#         self.fields['code_string'].widget.attrs['class'] = 'input-lg form-control'
#
#     code_string = forms.CharField()
#
#     def clean_code_string(self):
#         """
#         Verify that:
#         (1) Code exists
#         (2) Code hasn't been used before by the submitter
#         (3) Code hasn't been used before by another user
#         (4) User doesn't have another code (of same or greater value) in the same activity
#         """
#         # Format the code string
#         code = self.cleaned_data['code_string'].upper().replace(" ", "").replace("-", "")
#         # self.code = self.code.upper().replace(" ", "").replace("-", "")
#
#         # Check that code exists
#         if not Code.objects.filter(code_string=code).exists():
#             raise ValidationError(u"%s ليس رمزًا صحيحًا" % code, code="invalid")
#         # If it does, get it for further validation
#         code = Code.objects.get(code_string=code)
#         self.instance = code
#         if code.user == self.user:
#             raise ValidationError(u"لقد استخدمت الرمز %s من قبل؛ لا يمكنك استخدامه مرة أخرى." % code, code="used")
#         if code.user is not None:
#             raise ValidationError(u"الرمز %s غير متوفر." % code,
#                                   code="unavailable")
#         # Check that user has another code in the same activity
#         if Code.objects.filter(activity=code.activity, user=self.user).exists():
#             if Code.objects.get(activity=code.activity, user=self.user).category.points >= code.category.points:
#                 raise ValidationError(u"لديك رمز آخر مسجل في نفس النشاط؛ لا يمكنك إدخال أكثر من رمز لنشاط واحد.",
#                                       code="has_other")
#             else:
#                 raise ValidationError(u"User has another code (of less value) in the same activity.",
#                                       code="has_other_less")
#         return code
#
#     class Meta:
#         model = Code
#         fields = ['code_string']