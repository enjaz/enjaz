from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from forms_builder.forms.models import Form


class Events(models.Model):
    activity= models.ForeignKey('Activity')
    
    
    submission_date= models.DateField(verbose_name= "Envent date")
    start_time= models.TimeField(verbose_name= "Starting time")
    end_time= models.TimeField(verbose_name= "Ending time")
    name= models.CharField(max_length=200, verbose_name= "Event name")
    location= models.CharField(max_length=128, verbose_name= "Event location")
    short_description= models.CharField(max_length=128, verbose_name= "Short description of the event")
 

class Activity(models.Model):
    primary_club = models.ForeignKey('clubs.Club', null=True,
                                     on_delete=models.SET_NULL,
                                     related_name='primary_activity',
                                     verbose_name=u"النادي المنظم")
    secondary_clubs = models.ManyToManyField('clubs.Club', blank=True,
                                            related_name="secondary_activity",
                                            verbose_name=u"الأندية المتعاونة")
    chosen_reviewer_club = models.ForeignKey('clubs.Club', null=True,
                                             blank=True,
                                             on_delete=models.SET_NULL,
                                             related_name='chosen_reviewer_activities',
                                             verbose_name=u"الكلية المراجعة")
    name = models.CharField(max_length=200, verbose_name=u"اسم النشاط")
    description = models.TextField(verbose_name=u"وصف النشاط")
    public_description = models.TextField(verbose_name=u"الوصف الإعلامي",
                                          help_text=u"هذا هو الوصف الذي سيعرض للطلاب")
    goals = models.TextField(verbose_name=u"ما أهداف هذا النشاط، وكيف يخدم المجتمع والصالح العام؟")
    requirements = models.TextField(blank=True,
                                    verbose_name=u"متطلبات النشاط الأخرى")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    is_editable = models.BooleanField(default=True, verbose_name=u"هل يمكن تعديله؟")
    is_deleted = models.BooleanField(default=False, verbose_name=u"محذوف؟")
    inside_collaborators = models.TextField(blank=True,
                                            verbose_name=u"المتعاونون من داخل الجامعة")
    outside_collaborators = models.TextField(blank=True,
                                             verbose_name=u"المتعاونون من خارج الجامعة")
    participants = models.IntegerField(verbose_name=u"عدد المشاركين",
                                       help_text=u"العدد المتوقع للمستفيدين من النشاط")
    category = models.ForeignKey('Category', null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name=u"التصنيف",
                                 # If they category has sub-categories, don't show it.
                                 limit_choices_to={'category__isnull': True})
    organizers = models.IntegerField(verbose_name=u"عدد المنظمين",
                                       help_text=u"عدد الطلاب الذين سينظمون النشاط")
    forms = GenericRelation(Form)
    assignee = models.ForeignKey('clubs.Club', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='assigned_activities',
                                 verbose_name=u"النادي المسند")
    gender_choices = (
        ('', u'الجميع'),
        ('F', u'الطالبات'),
        ('M', u'الطلاب'),
        )
    gender = models.CharField(max_length=1,verbose_name=u"النشاط موجه ل",
                              choices=gender_choices, default="",
                              blank=True)
    is_approved_choices = (
        (True, u'معتمد'),
        (False, u'مرفوض'),
        (None, u'معلق'),
        )
    is_approved = models.NullBooleanField(verbose_name=u"الحالة",
                                          choices=is_approved_choices)
