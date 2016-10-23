# -*- coding: utf-8  -*-
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from tagging.registry import register
from tagging_autocomplete.models import TagAutocompleteField
from core.models import StudentClubYear
from bulb import managers
from niqati.models import Code
import accounts.utils
import niqati.utils


class Category(models.Model):
    name = models.CharField(max_length=50,
                               verbose_name=u"اسم التصنيف")
    code_name = models.CharField(max_length=50,
                                 verbose_name=u"الاسم البرمجي",
                                 help_text=u"حروف لاتينية صغيرة وأرقام")
    is_meta = models.BooleanField(default=False,
                                  verbose_name=u"تصنيف علوي؟")
    description = models.TextField(blank=True, verbose_name=u"وصف التصنيف")
    image = models.ImageField(upload_to='bulb/categories/', blank=True, null=True)
    def __unicode__(self):
        return self.name

class NeededBook(models.Model):
    tags = TagAutocompleteField(u"الوسوم")
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    title = models.CharField(u"العنوان", max_length=200)
    cover = models.ImageField(u"الغلاف", upload_to='bulb/covers/')
    authors = models.CharField(u"تأليف", max_length=200)
    description = models.TextField(u"وصف الكتاب")
    requester = models.ForeignKey(User)
    category = models.ForeignKey(Category,
                                 verbose_name=u"القسم",
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'is_meta': False})
    existing_book = models.ForeignKey('Book', null=True,
                                      on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)
    objects = managers.NeededBookQuerySet.as_manager()

#register(NeededBook)
    
class Book(models.Model):
    tags = TagAutocompleteField(u"الوسوم")
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    pages = models.PositiveSmallIntegerField(u"عدد الصفحات",
                                             blank=True, null=True, help_text=u"اختياري")
    title = models.CharField(max_length=200, verbose_name=u"العنوان")
    authors = models.CharField(max_length=200, verbose_name=u"تأليف")
    edition = models.CharField(max_length=200, verbose_name=u"الطبعة",
                               blank=True, help_text=u"اختياري")
    condition_choices = (
        ('N', u'كأنه جديد'),
        ('VG', u'جيدة جدا'),
        ('G', u'جيدة'),
        ('P', u'دون الجيدة'),
        )
    condition = models.CharField(max_length=2, verbose_name=u"حالة الكتاب",
                                 choices=condition_choices,
                                 help_text=u"هل من صفحات ناقصة أو ممزقة مثلا؟")
    contribution_choices = (
        ('L', u'إعارة'),
        ('G', u'اقتناء'),
    )
    contribution = models.CharField(max_length=1, default='G',
                                    verbose_name=u"نوع المساهمة",
                                    choices=contribution_choices)
    available_until = models.DateField(u"متاح حتى",
                                      null=True, blank=True,
                                      help_text=u"الكتاب متاح للاستعارة حتى تاريخ محدد (اختياري)")
    description = models.TextField(verbose_name=u"وصف الكتاب")
    submitter = models.ForeignKey(User,
                                  related_name='book_giveaways')
    cover = models.ImageField(u"الغلاف", upload_to='bulb/covers/')
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)
    category = models.ForeignKey(Category,
                                 verbose_name=u"القسم",
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'is_meta': False})
    is_publicly_owned = models.BooleanField(default=False,
                                            verbose_name=u"كتاب عمومي لا يُنسب لحساب بعينه.")
    is_available = models.BooleanField(default=True,
                                       verbose_name=u"متاح؟")
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوف؟")
    objects = managers.BookQuerySet.as_manager()


    def is_in_user_city(self, user):
        if user.is_superuser:
            return True
        else:
            return accounts.utils.get_user_city(user) == accounts.utils.get_user_city(self.submitter)

    def last_pending_request(self):
        if self.contribution == 'L':
            pending_requests = self.request_set.filter(status__in=["", "D"]).order_by('-submission_date')
        elif self.contribution == 'G':
            pending_requests = self.request_set.filter(status="").order_by('-submission_date')
        if pending_requests.exists():
            return pending_requests.first()

    def is_within_availability_period(self):
        if self.available_until:
            return self.available_until > timezone.now().date()
        else:
            return True

    def __unicode__(self):
        return self.title

#register(Book)

class Request(models.Model):
    book = models.ForeignKey(Book, null=True,
                             on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    requester = models.ForeignKey(User)
    delivery_choices = (
        ('D', u'إيصال مباشر'),
        ('I', u'إيصال غير مباشر'),
        )
    delivery = models.CharField(max_length=1, verbose_name=u"نوع التسليم",
                                choices=delivery_choices)
    status_choices = (
        ('', u'معلقة'),
        ('D', u'سلم لطالبه'),
        ('F', u'تعذّر'),
        ('C', u'ملغى'),
        ('R', u'أعيد بعد الإعارة'),
    )
    status = models.CharField(max_length=1, verbose_name=u"الحالة العامة",
                              choices=status_choices, default="",
                              blank=True)
    requester_status = models.CharField(max_length=1, verbose_name=u"حالة مقدم الطلب",
                                        choices=status_choices, default="",
                                        blank=True)
    requester_status_date = models.DateTimeField(u"تاريخ تأكيد مقدم الطلب",
                                             blank=True, default=None,
                                             null=True)
    owner_status = models.CharField(max_length=1, verbose_name=u"حالة صاحب الكتاب",
                                    choices=status_choices, default="",
                                    blank=True)
    owner_status_date = models.DateTimeField(u"تاريخ تأكيد صاحب الكتاب",
                                             blank=True, default=None,
                                             null=True)
    borrowing_end_date = models.DateField(u"تاريخ انتهاء مدة الإعارة",
                                          blank=True, default=None,
                                          null=True)
    objects = managers.RequestQuerySet.as_manager()

    def get_expected_delivery_date(self):
        return self.submission_date + timedelta(7)

    def get_cancellation_date(self):
        return (self.submission_date + timedelta(10)).date()

    def cancel_related_user_point(self, user):
        point = Point.objects.filter(request=self,
                                     user=user,
                                     is_counted=True)\
                             .update(is_counted=False)

    def create_related_niqati_codes(self, random_string=None):
        # Skip owner niqati if the book is publicly owned
        if not niqati.utils.can_claim_niqati(self.book.submitter) or \
           self.book.is_publicly_owned:
            return
        current_year = StudentClubYear.objects.get_current()
        if not random_string:
            random_strings = niqati.utils.get_free_random_strings(1)
            random_string = random_strings[0]
        request_content_type = ContentType.objects.get(app_label="bulb", model="request")
        owner_codes = Code.objects.filter(user=self.book.submitter,
                                          content_type=request_content_type,
                                          object_id=self.pk)
        if not owner_codes.exists():
            Code.objects.create(user=self.book.submitter,
                                content_object=self,
                                string=random_string,
                                year=current_year,
                                points=1,
                                redeem_date=timezone.now())

    def create_related_points(self):
        current_year = StudentClubYear.objects.get_current()
        requester_points = Point.objects.filter(request=self,
                                                user=self.requester,
                                                is_counted=True)

        if not requester_points.exists():
            Point.objects.create(year=current_year,
                                 category=self.book.contribution,
                                 request=self,
                                 user=self.requester,
                                 value=-1)

        # Skip owner points if the book is publicly owned
        if self.book.is_publicly_owned:
            return

        owner_points = Point.objects.filter(request=self,
                                            user=self.book.submitter,
                                            is_counted=True)
        if not owner_points.exists():
            Point.objects.create(year=current_year,
                                 category=self.book.contribution,
                                 request=self,
                                 user=self.book.submitter,
                                 value=1)

    def is_due_returning(self):
        return timezone.now().date() >= self.borrowing_end_date

    def __unicode__(self):
        return self.book.title

class Point(models.Model):
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL,
                             verbose_name=u"السنة")
    request = models.ForeignKey(Request, null=True, blank=True,
                                verbose_name=u"الطلب")
    user = models.ForeignKey(User, verbose_name=u"المستخدم",
                             related_name="book_points")
    category_choices = (
        ('L', u'استعارة'),
        ('G', u'اقتناء'),
    )
    category = models.CharField(u"التصنيف", max_length=1,
                                choices=category_choices,
                                default="G")
    is_counted = models.BooleanField(u"محسوبة؟", default=True)
    note = models.CharField(u"ملاحظة", max_length=50,
                            blank=True, default="")
    value = models.IntegerField(u"القيمة")

    objects = managers.PointQuerySet.as_manager()

    def get_details(self):
        if self.request and self.user == self.request.requester:
            message =  u"طلبت الكتاب"
        elif self.request and self.user == self.request.book.submitter:
            message = u"ساهمت بالكتاب."
        else:
            message = self.note
        if self.value == 2:
            message += u" (رصيد مُحوّل من الاقتناء للاستعارة)"
        return message

    def __unicode__(self):
        return "%s (%s)" % (self.user.username, self.value)
    
class Group(models.Model):
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL)
    image = models.ImageField(u"الصورة", upload_to='bulb/groups/')
    name = models.CharField(max_length=200, verbose_name=u"الاسم")
    description = models.TextField(verbose_name=u"وصف")
    coordinator = models.ForeignKey(User, null=True,
                                    verbose_name=u"المنسق",
                                    related_name="reading_group_coordination",
                                    on_delete=models.SET_NULL,
                                    limit_choices_to={'common_profile__is_student':
                                                        True})
    is_limited_by_gender = models.BooleanField(u"محدودة بالجندر", default=True)
    is_limited_by_city = models.BooleanField(u"محدودة بالمدينة", default=True)
    category = models.ForeignKey(Category,
                                 verbose_name=u"التصنيفات",
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'is_meta': False})
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)
    is_private = models.BooleanField(default=False,
                                     verbose_name=u"هل المجموعة خاصة وتطلب موافقة قبل النضمام والاطلاع؟")
    is_archived = models.BooleanField(default=False,
                                     verbose_name=u"مؤرشفة؟")
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوفة؟")

    objects = managers.GroupQuerySet.as_manager()

    def is_mixed_gender(self):
        """Check if the group has active memberships of different genders."""
        return not self.membership_set.active()\
                                      .exclude(user__commmon_profile__college__gender=self.coordinator.common_profile.college.gender)\
                                      .exists()

    def get_last_session(self):
        try:
            return self.session_set.filter(is_deleted=False).order_by('date').last()
        except Session.DoesNotExist:
            return

    def get_has_recent_sessions(self):
        three_weeks_ago = timezone.now().date() - timedelta(21)
        return self.session_set.filter(is_deleted=False).filter(date__gte=three_weeks_ago).exists()

    def get_report_count(self):
        return Report.objects.filter(session__group=self).count()

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    group = models.ForeignKey(Group, verbose_name=u"المجموعة")
    user = models.ForeignKey(User, null=True,
                             blank=True,
                             verbose_name=u"المنسق",
                             related_name="reading_group_memberships",
                             on_delete=models.SET_NULL,
                             limit_choices_to={'common_profile__is_student':
                                               True})
    is_active = models.BooleanField(default=True,
                                     verbose_name=u"مفعلة؟")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    modification_date = models.DateTimeField(u"تاريخ التعديل",
                                           auto_now=True)

    objects = managers.MembershipQuerySet.as_manager()

    def __unicode__(self):
        return "%s - %s" % (self.group.name, self.user.username)

class Session(models.Model):
    year = models.ForeignKey('core.StudentClubYear', null=True,
                             on_delete=models.SET_NULL, blank=True)
    group = models.ForeignKey(Group, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"المجموعة")
    title = models.CharField(max_length=200, verbose_name=u"عنوان الجلسة")
    agenda = models.TextField(verbose_name=u"محاور الجلسة")
    location = models.CharField(blank=True, default="",
                                max_length=200,
                                verbose_name=u"المكان")
    date = models.DateField(u"التاريخ")
    start_time = models.TimeField(u"وقت البداية")
    end_time = models.TimeField(u"وقت النهاية")
    is_limited_by_gender = models.BooleanField(u"محدودة بالجندر", default=True)
    is_limited_by_city = models.BooleanField(u"محدودة بالمدينة", default=True)
    is_deleted = models.BooleanField(default=False,
                                     verbose_name=u"محذوفة؟")
    submitter = models.ForeignKey(User, null=True, blank=True,
                                  related_name="sessions_submitted")
    confirmed_attendees = models.ManyToManyField(User, blank=True,
                                            related_name="sessions_confirmed")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    is_online = models.BooleanField(default=False,
                                    verbose_name=u"جلسة الإنترنت؟")
    objects = managers.SessionQuerySet.as_manager()

    def __unicode__(self):
        if self.group:
            return "%s (%s)" % (self.group.name, self.title)
        else:
            return self.title

class Report(models.Model):
    session = models.OneToOneField(Session, null=True,
                                   on_delete=models.SET_NULL,
                                   verbose_name=u"الجلسة")
    attendees = models.ManyToManyField(User, blank=True,
                                     related_name="reading_group_attendance",
                                     limit_choices_to={'common_profile__is_student': True})
    description = models.TextField(verbose_name=u"مجريات الجلسة")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)

    def create_related_niqati_codes(self):
        current_year = StudentClubYear.objects.get_current()
        session_content_type = ContentType.objects.get(app_label="bulb", model="session")
        coordinator = self.session.group.coordinator
        attendees = self.attendees.all() | \
                    User.objects.filter(pk=coordinator.pk)
        code_count = attendees.count()
        random_strings = niqati.utils.get_free_random_strings(code_count)
        string_count = 0

        # Attendees can have three statuses:
        # 1) A coordinator who is hosting their first session (=3 points)
        # 2) A coordinator who is hosting their further session (=2 points)
        # 3) An attednees

        for attendee in attendees:
            if not niqati.utils.can_claim_niqati(attendee):
                continue
            if attendee == coordinator:
                if self.session.group.session_set.filter(is_deleted=False).order_by("date").first() == self.session:
                    points = 3
                else:
                    points = 2
            else:
                points = 1
            attendee_codes = Code.objects.filter(user=attendee,
                                                 content_type=session_content_type,
                                                 object_id=self.session.pk)
            if not attendee_codes.exists():
                Code.objects.create(user=attendee,
                                    content_object=self.session,
                                    string=random_strings[string_count],
                                    year=current_year,
                                    points=points,
                                    redeem_date=self.submission_date)
            string_count += 1

    def __unicode__(self):
        return "%s %d" % (self.session.group.name, self.pk)


class ReaderProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=u"المستخدم",
                                related_name="reader_profile")
    areas_of_interests = models.TextField(verbose_name=u"مجالات اهتمامك",
                                          help_text=u"فيم تفضل القراءة؟")
    favorite_books = models.TextField(verbose_name=u"كتبك المفضّلة.",
                                      help_text=u"من أفضل الكتب التي قرأت، اختر ثلاثة!")
    favorite_writers  = models.TextField(verbose_name=u"كُتابك وكاتباتك المفضلين",
                                        help_text=u"من أفضل الذين قرأت لهم، اختر ثلاثة!")
    average_reading = models.CharField(max_length=200, verbose_name=u"معدل القراءة",
                                       help_text=u"كم كتابا تقرأ في السنة؟")
    goodreads = models.CharField(max_length=200, verbose_name=u"حساب Goodreads؟",
                                 help_text=u"هل لديك حساب على موقع Goodreads؟ (اختياري)",
                                 blank=True)
    twitter = models.CharField(max_length=200, verbose_name=u"حساب تويتر؟",
                                      help_text=u"هل لديك حساب على تويتر؟ (اختياري)",
                                      blank=True)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True,
                                           null=True)

    def __unicode__(self):
        return self.user.username

class Recruitment(models.Model):
    user = models.ForeignKey(User, verbose_name=u"المستخدم",
                             related_name="bulb_recruitment")
    prefers_coordination = models.BooleanField(default=False)
    prefers_team_membership = models.BooleanField(default=False)
    prefers_alone = models.BooleanField(default=False)

    # Book exchange
    wants_book_contribution = models.BooleanField(default=False)
    book_estimate = models.PositiveIntegerField(blank=True, null=True)
    wants_book_exchange_organization = models.BooleanField(default=False)

    # Reading group
    reading_group_subjects = models.TextField(blank=True)
    wants_reading_group_coordination = models.BooleanField(default=False)
    wants_reading_group_organization = models.BooleanField(default=False)

    # Debates
    debate_subjects = models.TextField(blank=True)
    watns_debate_participation = models.BooleanField(default=False)
    wants_debate_organization = models.BooleanField(default=False)

    # Dewanya
    dewanya_subjects = models.TextField(blank=True)
    dewanya_guests = models.TextField(blank=True)
    wants_dewanya_organization = models.BooleanField(default=False)

    # Media
    wants_media_design = models.BooleanField(default=False)
    example_design = models.FileField(upload_to="bulb_design_examples", blank=True)
    wants_media_video = models.BooleanField(default=False)
    wants_media_photography = models.BooleanField(default=False)

    # Getting to know them
    interests = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    activities = models.TextField(blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    goodreads = models.URLField(blank=True)

    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    def __unicode__(self):
        return self.user.username

class NewspaperSignup(models.Model):
    user = models.OneToOneField(User, verbose_name=u"المستخدم",
                                related_name="bulb_newspaper_signup",
                                null=True, blank=True)
    email = models.EmailField(default="", blank=True)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                       auto_now_add=True)

    def get_email(self):
        return self.email or self.user.email

    def __unicode__(self):
        return self.email or self.user.username

class DewanyaSuggestion(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"الاسم")
    subject = models.CharField(max_length=100, verbose_name=u"الموضوع")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                       auto_now_add=True)    

class Readathon(models.Model):
    publication_date = models.DateTimeField(u"تاريخ النشر", null=True, blank=True)
    start_date = models.DateField(u"تاريخ البداية")
    end_date = models.DateField(u"تاريخ النهاية")
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)
    template_name = models.CharField(u"العنوان", max_length=200)
    objects = managers.ReadathonQuerySet.as_manager()

    def has_started(self):
        return timezone.now().date() > self.start_date

    def __unicode__(self):
        return self.start_date.strftime("%Y-%m-%d")

class BookCommitment(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=u"المستخدمـ/ـة")
    readathon = models.ForeignKey(Readathon,
                                  verbose_name=u"الريديثون")
    title = models.CharField(u"العنوان", max_length=200)
    cover = models.ImageField(u"الغلاف", upload_to='bulb/book_commitments/')
    reason = models.TextField(u"لماذا تودّ/ين قراءة هذا الكتاب في الريديثون؟", blank=True, help_text=u"بناء على هذه الإجابة، سيكون الاختيار لجلسة النقاش المصغرة.")
    wants_to_attend = models.BooleanField(u"تود/ين حضور جلسة النقاش المصغرة؟",
                                          default=False)
    wants_to_contribute = models.BooleanField(u"تود/ين المساهمة بمنتج ثقافي بعد إتمام خطّة القراءة؟",
                                              default=False)
    pages = models.PositiveSmallIntegerField(u"صفحات الكتاب",
                                             null=True)
    completed_pages = models.PositiveSmallIntegerField(u"صفحات الكتاب المكتملة",
                                                       null=True)
    is_deleted = models.BooleanField(u"هل حُذف؟",
                                     default=False)
    submission_date = models.DateTimeField(u"تاريخ الإرسال",
                                           auto_now_add=True)

    def get_progress_percentage(self):
        if self.pages and self.completed_pages:
            percentage =  float(self.completed_pages) / self.pages * 100
            return "{0:.0f}".format(percentage)
        else:
            return 0

    def __unicode__(self):
        return self.title
