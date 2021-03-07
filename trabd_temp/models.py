# -*- coding: utf-8  -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max
from django.utils import timezone


# Create your models here.
city_choices = (
    ('R', 'الرياض'),
    ('J', 'جدة'),
    ('A', 'الأحساء'),
    )

position_choices = (
    ('1R', 'رئيس نادي الطلاب'),
    ('2R', 'نائب رئيس نادي الطلاب في الرياض'),
    ('3R', 'نائبة رئيس نادي الطلاب في الرياض'),
    ('4R', 'رئيسـ/ـة المركز الإعلامي في الرياض'),
    ('6R', 'رئيس نادي كلية العلوم والمهن الصحية في الرياض'),
    ('7R', 'رئيسة نادي كلية العلوم والمهن الصحية في الرياض'),
    ('8R', 'رئيس نادي كلية الصحة العامة في الرياض'),
    ('9R', 'رئيسة نادي كلية الصحة العامة في الرياض'),
    ('10R', 'رئيس نادي كلية طب الأسنان في الرياض'),
    ('11R', 'رئيسة نادي كلية طب الأسنان في الرياض'),
    ('12R', 'رئيس نادي كلية الصيدلة في الرياض'),
    ('13R', 'رئيسة نادي كلية الصيدلة في الرياض'),
    ('14R', 'رئيس نادي كلية العلوم الطبية التطبيقية في الرياض'),
    ('15R', 'رئيسة نادي كلية العلوم الطبية التطبيقية في الرياض'),
    ('16R', 'رئيسة نادي كلية التمريض في الرياض'),
    ('17R', 'رئيس نادي كلية الطب في الرياض'),
    ('18R', 'رئيسة نادي كلية الطب في الرياض'),
    ('19R', 'رئيس نادي مشكاة في الرياض'),
    ('20R', 'رئيسة نادي مشكاة في الرياض'),
    ('21R', 'رئيس نادي لين في الرياض'),
    ('22R', 'رئيسة نادي لين في الرياض'),
    ('23R', 'رئيس نادي الفنون في الرياض'),
    ('24R', 'رئيسة نادي الفنون في الرياض'),
    ('25R', 'رئيس نادي الأمن السيبراني في الرياض'),
    ('26R', 'رئيسة نادي الأمن السيبراني في الرياض'),
    ('27R', 'رئيس نادي بصيرة في الرياض'),
    ('28R', 'رئيسة نادي بصيرة في الرياض'),
    ('29R', 'رئيس مبادرة أرشدني في الرياض'),
    ('30R', 'رئيسة مبادرة أرشدني في الرياض'),

    ('31R', 'ممثل المجلس الاستشاري كلية العلوم والمهن الصحية في الرياض'),
    ('32R', 'ممثلة المجلس الاستشاري كلية العلوم والمهن الصحية في الرياض'),
    ('33R', 'ممثل المجلس الاستشاري كلية الطب في الرياض'),
    ('34R', 'ممثلة المجلس الاستشاري كلية الطب في الرياض'),
    ('35R', 'ممثل المجلس الاستشاري كلية طب الأسنان في الرياض'),
    ('36R', 'ممثلة المجلس الاستشاري كلية طب الأسنان في الرياض'),
    ('42R', 'ممثل المجلس الاستشاري كلية الصيدلة في الرياض'),
    ('43R', 'ممثلة المجلس الاستشاري كلية الصيدلة في الرياض'),
    ('37R', 'ممثل  المجلس الاستشاري كلية العلوم الطبية التطبيقية في الرياض'),
    ('38R', 'ممثلة  المجلس الاستشاري كلية العلوم الطبية التطبيقية في الرياض'),
    ('39R', 'ممثلة المجلس الاستشاري كلية الصيدلة المجلس الاستشاري كلية التمريض في الرياض'),
    ('40R', 'ممثل المجلس الاستشاري كلية الصحة العامة في الرياض'),
    ('41R', 'ممثلة المجلس الاستشاري كلية الصحة العامة في الرياض'),
    ('44R', 'ممثلـ/ـة طلاب الامتياز في الرياض'),

    ('2J', 'نائب رئيس نادي الطلاب في جدة'),
    ('3J', 'نائبة رئيس نادي الطلاب في جدة'),
    ('4J', 'رئيسـ/ـة المركز الإعلامي في جدة'),
    ('6J', 'رئيس نادي كلية العلوم والمهن الصحية في جدة'),
    ('7J', 'رئيسة نادي كلية العلوم والمهن الصحية في جدة'),
    ('8J', 'رئيس نادي كلية الصحة العامة في جدة'),
    ('9J', 'رئيسة نادي كلية الصحة العامة في جدة'),
    ('10J', 'رئيس نادي كلية طب الأسنان في جدة'),
    ('11J', 'رئيسة نادي كلية طب الأسنان في جدة'),
    # ('12J', 'رئيس نادي كلية الصيدلة في جدة'),
    # ('13J', 'رئيسة نادي كلية الصيدلة في جدة'),
    ('14J', 'رئيس نادي كلية العلوم الطبية التطبيقية في جدة'),
    ('15J', 'رئيسة نادي كلية العلوم الطبية التطبيقية في جدة'),
    ('16J', 'رئيسة نادي كلية التمريض في جدة'),
    ('17J', 'رئيس نادي كلية الطب في جدة'),
    ('18J', 'رئيسة نادي كلية الطب في جدة'),
    ('19J', 'رئيس نادي مشكاة في جدة'),
    ('20J', 'رئيسة نادي مشكاة في جدة'),
    ('21J', 'رئيس نادي لين في جدة'),
    ('22J', 'رئيسة نادي لين في جدة'),
    ('23J', 'رئيس نادي الفنون في جدة'),
    ('24J', 'رئيسة نادي الفنون في جدة'),
    ('25J', 'رئيس نادي الأمن السيبراني في جدة'),
    ('26J', 'رئيسة نادي الأمن السيبراني في جدة'),
    ('27J', 'رئيس نادي بصيرة في جدة'),
    ('28J', 'رئيسة نادي بصيرة في جدة'),
    ('29J', 'رئيس مبادرة أرشدني في جدة'),
    ('30J', 'رئيسة مبادرة أرشدني في جدة'),

    ('31J', 'ممثل المجلس الاستشاري كلية العلوم والمهن الصحية في جدة'),
    ('32J', 'ممثلة المجلس الاستشاري كلية العلوم والمهن الصحية في جدة'),
    ('33J', 'ممثل المجلس الاستشاري كلية الطب في جدة'),
    ('34J', 'ممثلة المجلس الاستشاري كلية الطب في جدة'),
    ('35J', 'ممثل المجلس الاستشاري كلية طب الأسنان في جدة'),
    ('36J', 'ممثلة المجلس الاستشاري كلية طب الأسنان في جدة'),
    ('37J', 'ممثل  المجلس الاستشاري كلية العلوم الطبية التطبيقية في جدة'),
    ('38J', 'ممثلة  المجلس الاستشاري كلية العلوم الطبية التطبيقية في جدة'),
    ('39J', 'ممثلة المجلس الاستشاري كلية الصيدلة المجلس الاستشاري كلية التمريض في جدة'),
    ('40J', 'ممثل المجلس الاستشاري كلية الصحة العامة في جدة'),
    ('41J', 'ممثلة المجلس الاستشاري كلية الصحة العامة في جدة'),
    ('42J', 'ممثلـ/ـة طلاب الامتياز في جدة'),

    ('2A', 'نائب رئيس نادي الطلاب في الأحساء'),
    ('3A', 'نائبة رئيس نادي الطلاب في الأحساء'),
    ('4A', 'رئيسـ/ـة المركز الإعلامي في الأحساء'),
    ('6A', 'رئيس نادي كلية العلوم والمهن الصحية في الأحساء'),
    ('7A', 'رئيسة نادي كلية العلوم والمهن الصحية في الأحساء'),
    ('14A', 'رئيس نادي كلية العلوم الطبية التطبيقية في الأحساء'),
    ('15A', 'رئيسة نادي كلية العلوم الطبية التطبيقية في الأحساء'),
    ('16A', 'رئيسة نادي كلية التمريض في الأحساء'),
    ('19A', 'رئيس نادي مشكاة في الأحساء'),
    ('20A', 'رئيسة نادي مشكاة في الأحساء'),
    ('21A', 'رئيس نادي لين في الأحساء'),
    ('22A', 'رئيسة نادي لين في الأحساء'),
    ('23A', 'رئيس نادي الفنون في الأحساء'),
    ('24A', 'رئيسة نادي الفنون في الأحساء'),
    ('25A', 'رئيس نادي الأمن السيبراني في الأحساء'),
    ('26A', 'رئيسة نادي الأمن السيبراني في الأحساء'),
    ('27A', 'رئيس نادي بصيرة في الأحساء'),
    ('28A', 'رئيسة نادي بصيرة في الأحساء'),
    ('29A', 'رئيس مبادرة أرشدني في الأحساء'),
    ('30A', 'رئيسة مبادرة أرشدني في الأحساء'),

    ('31A', 'ممثل المجلس الاستشاري كلية العلوم والمهن الصحية في الأحساء'),
    ('32A', 'ممثلة المجلس الاستشاري كلية العلوم والمهن الصحية في الأحساء'),
    ('37A', 'ممثل  المجلس الاستشاري كلية العلوم الطبية التطبيقية في الأحساء'),
    ('38A', 'ممثلة  المجلس الاستشاري كلية العلوم الطبية التطبيقية في الأحساء'),
    ('39A', 'ممثلة المجلس الاستشاري كلية الصيدلة المجلس الاستشاري كلية التمريض في الأحساء'),
    ('40A', 'ممثلـ/ـة طلاب الامتياز في الأحساء'),

)

class Nomination(models.Model):
    plan = models.FileField("الخطة")
    cv = models.FileField("السيرة الذاتية")
    certificates = models.FileField(null=True, verbose_name="الشهادات والمساهمات")
    gpa = models.FloatField("المعدل الجامعي", null=True)
    user = models.ForeignKey(User, verbose_name="المرشَّح")
    position = models.CharField("المنصب", max_length=3, blank=True,
                                default="1R", choices=position_choices)
    city = models.CharField("المدينة", max_length=1, blank=True,
                            default="", choices=city_choices)
    is_rejected = models.BooleanField(default=False)
    submission_date = models.DateTimeField("تاريخ التقديم", auto_now_add=True)
    modification_date = models.DateTimeField("تاريخ التعديل", auto_now=True, null=True)

    class Meta:
        verbose_name = 'المرشحـ/ـة'
        verbose_name_plural = 'المرشحون/المرشّحات'

    def __unicode__(self):
        try:
            name = self.user.common_profile.get_ar_full_name()
        except ObjectDoesNotExist:
            # If no profile
            name = self.user.username
        return "nomination of %s for %s" % (name, self.position)