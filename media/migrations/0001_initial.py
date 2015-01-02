# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FollowUpReport'
        db.create_table(u'media_followupreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activities.Episode'], unique=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('organizer_count', self.gf('django.db.models.fields.IntegerField')()),
            ('participant_count', self.gf('django.db.models.fields.IntegerField')()),
            ('announcement_sites', self.gf('django.db.models.fields.TextField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['FollowUpReport'])

        # Adding model 'FollowUpReportImage'
        db.create_table(u'media_followupreportimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['media.FollowUpReport'])),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'media', ['FollowUpReportImage'])

        # Adding model 'ReportComment'
        db.create_table(u'media_reportcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['media.FollowUpReport'])),
        ))
        db.send_create_signal(u'media', ['ReportComment'])

        # Adding model 'Story'
        db.create_table(u'media_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activities.Episode'], unique=True)),
            ('writer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'media', ['Story'])

        # Adding model 'Article'
        db.create_table(u'media_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'authored_articles', to=orm['auth.User'])),
            ('author_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['Article'])

        # Adding model 'StoryReview'
        db.create_table(u'media_storyreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_reviewed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('approve', self.gf('django.db.models.fields.BooleanField')()),
            ('story', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['media.Story'], unique=True)),
        ))
        db.send_create_signal(u'media', ['StoryReview'])

        # Adding model 'ArticleReview'
        db.create_table(u'media_articlereview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_reviewed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('approve', self.gf('django.db.models.fields.BooleanField')()),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Article'])),
        ))
        db.send_create_signal(u'media', ['ArticleReview'])

        # Adding model 'StoryTask'
        db.create_table(u'media_storytask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assigner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_assigned', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('episode', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['activities.Episode'], unique=True)),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assigned_storytasks', to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['media.Story'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['StoryTask'])

        # Adding model 'CustomTask'
        db.create_table(u'media_customtask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assigner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_assigned', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assigned_tasks', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('completed_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['CustomTask'])

        # Adding model 'TaskComment'
        db.create_table(u'media_taskcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.CustomTask'])),
        ))
        db.send_create_signal(u'media', ['TaskComment'])

        # Adding model 'Poll'
        db.create_table(u'media_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll_type', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('open_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'media', ['Poll'])

        # Adding model 'PollChoice'
        db.create_table(u'media_pollchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['media.Poll'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('color', self.gf('django.db.models.fields.CharField')(default='green', max_length=128)),
        ))
        db.send_create_signal(u'media', ['PollChoice'])

        # Adding model 'PollResponse'
        db.create_table(u'media_pollresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['media.Poll'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.PollChoice'])),
        ))
        db.send_create_signal(u'media', ['PollResponse'])

        # Adding unique constraint on 'PollResponse', fields ['poll', 'user']
        db.create_unique(u'media_pollresponse', ['poll_id', 'user_id'])

        # Adding model 'PollComment'
        db.create_table(u'media_pollcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['media.Poll'])),
        ))
        db.send_create_signal(u'media', ['PollComment'])


    def backwards(self, orm):
        # Removing unique constraint on 'PollResponse', fields ['poll', 'user']
        db.delete_unique(u'media_pollresponse', ['poll_id', 'user_id'])

        # Deleting model 'FollowUpReport'
        db.delete_table(u'media_followupreport')

        # Deleting model 'FollowUpReportImage'
        db.delete_table(u'media_followupreportimage')

        # Deleting model 'ReportComment'
        db.delete_table(u'media_reportcomment')

        # Deleting model 'Story'
        db.delete_table(u'media_story')

        # Deleting model 'Article'
        db.delete_table(u'media_article')

        # Deleting model 'StoryReview'
        db.delete_table(u'media_storyreview')

        # Deleting model 'ArticleReview'
        db.delete_table(u'media_articlereview')

        # Deleting model 'StoryTask'
        db.delete_table(u'media_storytask')

        # Deleting model 'CustomTask'
        db.delete_table(u'media_customtask')

        # Deleting model 'TaskComment'
        db.delete_table(u'media_taskcomment')

        # Deleting model 'Poll'
        db.delete_table(u'media_poll')

        # Deleting model 'PollChoice'
        db.delete_table(u'media_pollchoice')

        # Deleting model 'PollResponse'
        db.delete_table(u'media_pollresponse')

        # Deleting model 'PollComment'
        db.delete_table(u'media_pollcomment')


    models = {
        u'activities.activity': {
            'Meta': {'object_name': 'Activity'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Category']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inside_collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organizers': ('django.db.models.fields.IntegerField', [], {}),
            'outside_collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'participants': ('django.db.models.fields.IntegerField', [], {}),
            'primary_club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_activity'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['clubs.Club']"}),
            'public_description': ('django.db.models.fields.TextField', [], {}),
            'requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secondary_clubs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_activity'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['clubs.Club']"}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        u'activities.category': {
            'Meta': {'object_name': 'Category'},
            'ar_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'en_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Category']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'activities.episode': {
            'Meta': {'object_name': 'Episode'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            'can_report_early': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'requires_report': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'requires_story': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'clubs.club': {
            'Meta': {'object_name': 'Club'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['clubs.College']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'coordination'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deputies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'deputyships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employee'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['auth.User']", 'blank': 'True', 'null': 'True'}),
            'english_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parenthood'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['clubs.Club']", 'blank': 'True', 'null': 'True'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'clubs.college': {
            'Meta': {'object_name': 'College'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'media.article': {
            'Meta': {'object_name': 'Article'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'authored_articles'", 'to': u"orm['auth.User']"}),
            'author_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'media.articlereview': {
            'Meta': {'object_name': 'ArticleReview'},
            'approve': ('django.db.models.fields.BooleanField', [], {}),
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.Article']"}),
            'date_reviewed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'media.customtask': {
            'Meta': {'object_name': 'CustomTask'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assigned_tasks'", 'to': u"orm['auth.User']"}),
            'assigner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_assigned': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'media.followupreport': {
            'Meta': {'object_name': 'FollowUpReport'},
            'announcement_sites': ('django.db.models.fields.TextField', [], {}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'episode': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['activities.Episode']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organizer_count': ('django.db.models.fields.IntegerField', [], {}),
            'participant_count': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'media.followupreportimage': {
            'Meta': {'object_name': 'FollowUpReportImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['media.FollowUpReport']"})
        },
        u'media.poll': {
            'Meta': {'object_name': 'Poll'},
            'close_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {}),
            'poll_type': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'media.pollchoice': {
            'Meta': {'object_name': 'PollChoice'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'green'", 'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['media.Poll']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'media.pollcomment': {
            'Meta': {'object_name': 'PollComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['media.Poll']"})
        },
        u'media.pollresponse': {
            'Meta': {'unique_together': "(('poll', 'user'),)", 'object_name': 'PollResponse'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.PollChoice']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': u"orm['media.Poll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'media.reportcomment': {
            'Meta': {'object_name': 'ReportComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['media.FollowUpReport']"})
        },
        u'media.story': {
            'Meta': {'object_name': 'Story'},
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['activities.Episode']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'writer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'media.storyreview': {
            'Meta': {'object_name': 'StoryReview'},
            'approve': ('django.db.models.fields.BooleanField', [], {}),
            'date_reviewed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'story': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['media.Story']", 'unique': 'True'})
        },
        u'media.storytask': {
            'Meta': {'object_name': 'StoryTask'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assigned_storytasks'", 'to': u"orm['auth.User']"}),
            'assigner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_assigned': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['activities.Episode']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['media.Story']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'media.taskcomment': {
            'Meta': {'object_name': 'TaskComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.CustomTask']"})
        }
    }

    complete_apps = ['media']