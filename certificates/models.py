# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File

from certificates import utils
from events.models import Abstract, Session
from niqati.utils import generate_random_string
import accounts.utils

TEXT_PLACE_HOLDER = 'Nada Abdullah'

class CertificateRequest(models.Model):
    submitter = models.ForeignKey(User, related_name="certificate_submissions")
    submitter_club = models.ForeignKey('clubs.Club', null=True, blank=True)
    episode = models.ForeignKey('activities.Episode', null=True, blank=True)
    description = models.CharField(u"وصف الشهادة", max_length=200)
    text = models.TextField(u"الصياغة")
    user_list = models.FileField(u"قائمة المستخدمين والمستخدمات", upload_to="certificate_lists", blank=True)
    users = models.ManyToManyField(User, blank=True, verbose_name=u"المستخدمون والمستخدمات")
    # Approval choices:
    #   None: Unreviewed
    #   True: Approved
    #   False: Rejected
    is_approved = models.NullBooleanField(default=None)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)

    def get_template(self):
        try:
            template = self.certificatetemplate
        except ObjectDoesNotExist:
            template = None
        return template

    def __unicode__(self):
        return self.description

class Certificate(models.Model):
    certificate_template = models.ForeignKey('CertificateTemplate',
                                             null=True, blank=True,
                                             verbose_name=u"القالب")
    user = models.ForeignKey(User, verbose_name=u"المستخدمـ/ـة")
    image = models.ImageField(u"الصورة")
    verification_code = models.CharField(u"رمز التحقق", max_length=6)

    description = models.CharField(u"وصف الشهادة", max_length=200,
                                   blank=True, default="")
    # A Certificate can bind to any model on Enjaz.  For now, it's
    # mainly a Session.
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                            auto_now=True)

    def regenerate_certificate(self, texts=None):
        if texts:
            self.texts.delete()
            # Let's save the text for further regeneration
            certificate_texts = []
            for text in texts:
                certificate_text = CertificateText(certificate=certificate,
                                                   text=text)
                certificate_texts.append(certificate_text)
            CertificateText.objects.bulk_create(certificate_texts)
            text_values = texts
        else:
            text_values = [text.text for text in self.texts.all()]
        file_path, relative_url = utils.generate_certificate_image(self.pk,
                                                                   template=self.certificate_template,
                                                                   texts=text_values,
                                                                   verification_code=self.verification_code)
        certificate_file = open(file_path)
        self.image.save("{}.{}".format(self.verification_code, self.image_format), File(certificate_file))

    def __unicode__(self):
        if self.description:
            return self.description

        name = accounts.utils.get_user_ar_full_name(self.user)
        if not name:
            name = self.user.username

        if type(self.content_object) is Session:
            return u"شهادة {} ل{}".format(name, self.content_object.name)
        elif type(self.content_object) is Abstract:
            if self.content_object.accepted_presentaion_preference == 'P':
                presentation_type = u"الملصق البحثي"
            elif self.content_object.accepted_presentaion_preference == 'O':
                presentation_type = u"التقديم الشفهي"
            else:
                presentation_type = u""
            return u"{} لبحث {}".format(presentation_type, self.content_object.title)
        elif self.certificate_template and self.certificate_template.certificate_request.description:
            return self.certificate_template.certificate_request.description
        else:
            return self.pk

class CertificateText(models.Model):
    certificate = models.ForeignKey(Certificate, verbose_name=u"الشهادة",
                                    related_name='texts')
    text = models.CharField(u"النص", max_length=200)

    def __unicode__(self):
        return self.text

class CertificateTemplate(models.Model):
    certificate_request = models.OneToOneField(CertificateRequest,
                                               blank=True, null=True)
    description = models.CharField(u"وصف الشهادة", max_length=200)
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

    def generate_certificate(self, user, texts, description="", content_object=None):
        while True:
            verification_code = generate_random_string(6)
            if not Certificate.objects.filter(verification_code=verification_code).exists():
                break

        file_path, relative_url = utils.generate_certificate_image(self.certificate_request.pk,
                                                                   template=self,
                                                                   texts=texts,
                                                                   verification_code=verification_code)
        certificate = Certificate.objects.create(certificate_template=self,
                                                 user=user,
                                                 description=description,
                                                 content_object=content_object,
                                                 verification_code=verification_code)

        # Let's save the text for further regeneration
        certificate_texts = []
        for text in texts:
            certificate_text = CertificateText(certificate=certificate,
                                               text=text)
            certificate_texts.append(certificate_text)
        CertificateText.objects.bulk_create(certificate_texts)

        # Let's save the certificate image
        certificate_file = open(file_path)
        certificate.image.save("{}.{}".format(verification_code, self.image_format), File(certificate_file))

        return certificate

    def __unicode__(self):
        return self.description

class TextPosition(models.Model):
    certificate_template = models.ForeignKey('CertificateTemplate',
                                             verbose_name=u"القالب",
                                             related_name="text_positions")
    y_position = models.PositiveIntegerField(u"الموضع على المحور السيني")
    x_center = models.BooleanField(u"انتصاف سيني", default=False)
    x_position = models.PositiveIntegerField(u"الموضع على المحور الصادي")
    y_center = models.BooleanField(u"انتصاف صادي", default=False)
    size = models.PositiveIntegerField(u"حجم الخط", default=34)
    color = models.CharField(u"لون الخط", max_length=10, default="000000")
    font_family = models.ForeignKey('FontFamily',
                                    verbose_name=u"الخطّ", null=True)

    def __unicode__(self):
        return "{}x{}".format(self.x_position, self.y_position)

class FontFamily(models.Model):
    name = models.CharField(u"اسم الخط", max_length=200)

    def __unicode__(self):
        return self.name
