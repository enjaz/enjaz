# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from certificates import utils
from niqati.utils import generate_random_string


TEXT_PLACE_HOLDER = 'Nada Abdullah'

class CertificateRequest(models.Model):
    submitter = models.ForeignKey(User, related_name="certificate_submissions")
    submitter_club = models.ForeignKey('clubs.Club', null=True, blank=True)
    episode = models.ForeignKey('activities.Episode', null=True, blank=True)
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
    certificate_template = models.ForeignKey('CertificateTemplate',
                                             verbose_name=u"القالب")
    user = models.ForeignKey(User, verbose_name=u"المستخدمـ/ـة")
    image = models.ImageField(u"الصورة")
    verification_code = models.CharField(u"رمز التحقق", max_length=6)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)

    def __unicode__(self):
        return u"{} ({})".format(self.certificate_template.certificate_request.description, self.user.username)

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

    def generate_certificate(self, user, text):
        template_bytes = self.image.read()
        while True:
            verification_code = generate_random_string(6)
            if not Certificate.objects.filter(verification_code=verification_code).exists():
                break

        file_path, relative_url = utils.generate_certificate_image(self.certificate_request.pk,
                                                                   template=self,
                                                                   template_bytes=template_bytes,
                                                                   text=text)
        certificate = Certificate.objects.create(certificate_template=self,
                                                 user=user,
                                                 verification_code=verification_code)
        certificate_file = open(file_path)
        certificate.image.save("{}.{}".format(certificate.pk, self.image_format), File(certificate_file))

        return certificate

    def __unicode__(self):
        return self.description

class TextPosition(models.Model):
    certificate_template = models.ForeignKey('CertificateTemplate',
                                             verbose_name=u"القالب",
                                             related_name="text_positions")
