# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

class Voice(models.Model):
    # A Voice is both: a parent Voice, or a reply Voice (i.e. comment
    # on a voice).  It could have been two different models but since
    # both of them are expceted to have comments and replies, it would
    # complicate things even further to separate them.
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المرسل", blank=True)
    title = models.CharField(max_length=100, verbose_name=u"العنوان",
                             blank=True)
    text = models.TextField(u"النص")
    recipient = models.CharField(max_length=50, verbose_name=u"موجه إلى",
                                 blank=True)
    is_published_choices = (
        (None, u'لم يراجع بعد'),
        (True, u'منشور'),
        (False, u'محذوف'),
        )
    is_published = models.NullBooleanField(verbose_name=u"منشور؟",
                                           default=True,
                                           choices=is_published_choices)
    is_editable = models.BooleanField(verbose_name=u"يمكن تعديله؟",
                                      default=True)
    # Yes, all the following three fields could have been calculated
    # dynamically, but it'd impair sorting making it memory-consuming.
    score = models.IntegerField(verbose_name=u"الدرجة", default=0)
    number_of_views = models.IntegerField(verbose_name=u"المشاهدات",
                                         default=0)
    number_of_comments = models.IntegerField(verbose_name=u"التعليقات",
                                             default=0)
    parent = models.ForeignKey('self', null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"رد على", blank=True,
                              related_name='replies')
    submission_date = models.DateTimeField(u'تاريخ النشر',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)

    def update_score(self):
        new_score = 0
        for vote in self.vote_set.filter(is_counted=True):
            if vote.vote_type == 'U':
                new_score += 1
            elif vote.vote_type == 'D':
                new_score -= 1
        self.score = new_score
        self.save()
        return new_score

    def update_views(self):
        new_views = self.view_set.filter(is_counted=True).count()
        self.number_of_views = new_views
        self.save()
        return new_views

    def update_comments(self):
        new_comments = 0
        replies = list(self.replies.filter(is_published=True))
        # Count all the whole comment hierarchy.
        while replies:
            for comment in replies:
                new_comments += 1
                if comment.replies:
                    replies += list(comment.replies.filter(is_published=True))
                comment_index = replies.index(comment)
                replies.pop(comment_index)
        self.number_of_comments = new_comments
        self.save()
        return new_comments

    def get_greatest_parent(self):
        """
In case of comments and subcomments, this returns the original
'voice' (aka thread).
        """
        if not self.parent:
            return self
        else:
            current_parent = self.parent
            while True:
                if not current_parent.parent:
                    break
                else:
                    current_parent = current_parent.parent
        return current_parent

    def is_reported(self):
        return bool(self.vote_set.filter(is_counted=True,
                                         vote_type='R'))
    is_reported.boolean = True
    is_reported.short_description = u"هل بُلّغ عنه؟"

    class Meta:
        verbose_name = u"صوت"
        verbose_name_plural = u"الأصوات"

    def __unicode__(self):
        return self.text

class Vote(models.Model):
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المصوت")
    voice = models.ForeignKey(Voice, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"الصوت")
    # Reports, for example, can be set to is_counted=False if the
    # reasoning is invalid.  Same goes with disabled/abusive users.
    is_counted = models.BooleanField(verbose_name=u"محسوب؟",
                                     default=True)
    vote_type_choices = (
        ('U', u'مع'),
        ('D', u'ضد'),
        ('R', u'بلاغ'),
        )
    vote_type = models.CharField(max_length=1,
                                 choices=vote_type_choices)
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)
    edit_date = models.DateTimeField('date edited', auto_now=True)

    class Meta:
        verbose_name = u"اقتراع"
        verbose_name_plural = u"الاقتراعات"

    def __unicode__(self):
        return "%s-%s-%s" % (self.submitter.username, self.vote_type,
                             self.voice.id)

class Response(models.Model):
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المجيب")
    voice = models.OneToOneField(Voice, null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name=u"الصوت")
    text = models.TextField(u"النص")
    is_published = models.BooleanField(verbose_name=u"منشور؟",
                                       default=True)
    is_editable = models.BooleanField(verbose_name=u"يمكن تعديله؟",
                                      default=True)
    submission_date = models.DateTimeField('date submitted',
                                           auto_now_add=True)
    edit_date = models.DateTimeField('date edited', auto_now=True)

    class Meta:
        verbose_name = u"استجابة"
        verbose_name_plural = u"الاستجابات"

class View(models.Model):
    viewer = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL,
                               verbose_name=u"المشاهد")
    is_counted = models.BooleanField(verbose_name=u"محسوبة؟",
                                     default=True)
    voice = models.ForeignKey(Voice, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"الصوت")
    view_date = models.DateTimeField('date viewed',
                                     auto_now_add=True)

    class Meta:
        verbose_name = u"مشاهدة"
        verbose_name_plural = u"المشاهدات"
