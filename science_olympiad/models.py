# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.db import models

from multiselectfield import MultiSelectField

invention_categories = (
    ('anm', 'علوم الحيوان'),
    ('bhv', 'العلوم الاجتماعية والسلوكية'),
    ('bch', 'الكيمياء الحيوية'),
    ('bmd', 'العلوم الطبية الحيوية والصحية'),
    ('mde', 'الهندسة الطبية الحيوية'),
    ('cbi', 'الأحياء الخلوية والجزيئية'),
    ('chm', 'الكيمياء'),
    ('bit', 'المعلوماتية الحيوية'),
    ('eco', 'علوم الأرض والبيئة'),
    ('emb', 'الأنظمة المدمجة'),
    ('che', 'الطاقة الكيميائية'),
    ('phe', 'الطاقة الفيزيائية'),
    ('mch', 'الهندسة الميكانيكية'),
    ('ene', 'الهندسة البيئية'),
    ('smt', 'علم المواد'),
    ('mat', 'الرياضيات'),
    ('mbi', 'الأحياء الدقيقة'),
    ('ast', 'الفيزياء والفلك'),
    ('bot', 'علوم النبات'),
    ('rai', 'الربوتات والذكاء الاصطناعي'),
    ('prg', 'الأنظمة البرمجية والبرمجة'),
    ('mob', 'العلوم الطبية الانتقالية'),
    ('oth', 'تصنيف آخر')
)

class Inventor(models.Model):
    ar_name = models.CharField(u"الاسم الثلاثي باللغة العربية", max_length=200)
    en_name = models.CharField(u"الاسم الثلاثي باللغة الإنجليزية", max_length=200)
    job = models.CharField(u"الوظيفة", max_length=200)
    workplace = models.CharField(u"جهة العمل/الدراسة", max_length=200)
    invention_name = models.CharField(u"اسم الاختراع", max_length=600)
    inv_category = MultiSelectField(u'التصنيف (يمكن اختيار أكثر من تصنيف)', choices=invention_categories)
    other_category = models.CharField(u"إذا اخترت 'تصنيف آخر'، اذكره هنا ", max_length=600, blank=True, null=True)
    summary = models.TextField(u"ملخص الاختراع")
    is_prototype = models.BooleanField(u"هل يوجد لديك نموذج أولي؟")
    prototype_file = models.FileField(u"الرجاء إرفاق النموذج الأولي كملف PDF إن وجد", blank=True, null=True)
    submission_date = models.DateTimeField(u'تاريخ التسجيل', auto_now_add=True)

    class Meta:
        verbose_name = u"مخترع"
        verbose_name_plural = u"مخترعين"

    def __unicode__(self):
        return self.invention_name

class ContestQuestion(models.Model):
    text = models.TextField(u'نص السؤال')
    category = models.CharField(u'نص السؤال', max_length=100)
    olympiad_version = models.CharField(u'نسخة الأولمبياد', max_length=100, null=True) #May be used later in life

    class Meta:
        verbose_name = u"سؤال"
        verbose_name_plural = u"أسئلة"

    def __unicode__(self):
        return self.text

class ContestAnswer(models.Model):
    question = models.ForeignKey(ContestQuestion, verbose_name=u'السؤال')
    text = models.TextField(u'نص الجواب')
    is_correct = models.BooleanField(u'هل الجواب صحيح؟', default=False)

    class Meta:
        verbose_name = u"جواب"
        verbose_name_plural = u"أجوبة"

    def __unicode__(self):
        return self.text
