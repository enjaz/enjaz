# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from activities.models import Episode
from clubs.models import Club
from colorfield.fields import ColorField
from niqati.utils import generate_random_string


class CertificateRequest(models.Model):
    submitter = models.ForeignKey(User, related_name="certificate_submissions")
    submitter_club = models.ForeignKey(Club, null=True, blank=True)
    episode = models.ForeignKey(Episode, null=True, blank=True)
    description = models.CharField(u"وصف الشهادة", max_length=200)
    text = models.TextField(u"الصياغة")
    student_list = models.FileField(u"قائمة الطلاب والطالبات", upload_to="certificate_lists", blank=True)
    students = models.ManyToManyField(User, blank=True, verbose_name=u"الطلاب والطالبات")
    # Approval choices:
    #   None: Unreviewed
    #   True: Approved
    #   False: Rejected
    is_approved = models.NullBooleanField(default=None)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)
    def __unicode__(self):
        return self.description

class Certificate(models.Model):
    certificate_template = models.ForeignKey('CertificateTemplate')
    email = models.EmailField(blank=True, default="")
    user = models.ForeignKey(User)
    image = models.ImageField()
    verification_code = models.CharField(u"رمز التحقق", max_length=6)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)

    def is_student_recipient(self):
        try:
            if self.user:
                return True
        except ObjectDoesNotExist:
            if self.email:
                return self.email.endswith("ksau-hs.edu.sa") or \
                       User.objects.filter(common_profile__alternative_email__iexact=self.email).exists()

    def get_user(self):
        try:
            if self.user:
                return True
        except ObjectDoesNotExist:
            if self.email:
                return (User.objects.filter(email__iexact=self.email) | \
                        User.objects.filter(common_profile__alternative_email__iexact=self.email)).first()

    def __unicode__(self):
        recipient = self.email or self.user.username
        return u"{} ({})".format(self.certificate_template.certificate_request.description, recipient)

class CertificateTemplate(models.Model):
    certificate_request = models.OneToOneField(CertificateRequest)
    description = models.CharField(u"وصف الشهادة", max_length=200)
    font_family = models.CharField(u"نوع الخط", max_length=200)
    font_size = models.PositiveIntegerField(u"حجم الخط", default=34)
    color = models.CharField(u"لون الخط", max_length=10, default="000000")
    y_position = models.PositiveIntegerField(u"الموضع على المحور السيني")
    x_position = models.PositiveIntegerField(u"الموضع على المحور الصادي")
    image = models.ImageField(u"صورة القالب", upload_to="certificate_templates")
    image_format_choices = (
        ('PNG', 'PNG'),
        ('GIF', 'GIF'),
        ('JPG', 'JPG'),
        )
    image_format = models.CharField(u"نسق الصورة", max_length=10,
                                    choices=image_format_choices,
                                    default="PNG")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)

    def generate_certificates(self):
        certificates = []
        if self.certificate_request.students.exists():
            for student in self.certificate_request.students.all():
                verification_code = generate_random_string(6)
                Certificate(certificate_template=self, user=student,
                            verification_code=verification_code)
        

    def __unicode__(self):
        return self.certificate_request.description
