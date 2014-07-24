# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MyProfile'
        db.delete_table(u'accounts_myprofile')

        # Adding model 'EnjazProfile'
        db.create_table(u'accounts_enjazprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='registered', max_length=15)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='enjaz_profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'accounts', ['EnjazProfile'])

        # Adding model 'NonStudentProfile'
        db.create_table(u'accounts_nonstudentprofile', (
            (u'enjazbaseprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.EnjazBaseProfile'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='nonstudent_profile', unique=True, to=orm['auth.User'])),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('job_description', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'accounts', ['NonStudentProfile'])

        # Adding model 'StudentProfile'
        db.create_table(u'accounts_studentprofile', (
            (u'enjazbaseprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.EnjazBaseProfile'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='student_profile', unique=True, to=orm['auth.User'])),
            ('student_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('college', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clubs.College'], null=True, on_delete=models.SET_NULL)),
        ))
        db.send_create_signal(u'accounts', ['StudentProfile'])

        # Adding model 'EnjazBaseProfile'
        db.create_table(u'accounts_enjazbaseprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ar_first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ar_middle_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ar_last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('en_first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('en_middle_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('en_last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('badge_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'accounts', ['EnjazBaseProfile'])


    def backwards(self, orm):
        # Adding model 'MyProfile'
        db.create_table(u'accounts_myprofile', (
            ('ar_first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('badge_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('college', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clubs.College'], null=True, on_delete=models.SET_NULL)),
            ('en_middle_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('en_last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('ar_middle_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='registered', max_length=15)),
            ('student_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ar_last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('en_first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='enjaz_profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'accounts', ['MyProfile'])

        # Deleting model 'EnjazProfile'
        db.delete_table(u'accounts_enjazprofile')

        # Deleting model 'NonStudentProfile'
        db.delete_table(u'accounts_nonstudentprofile')

        # Deleting model 'StudentProfile'
        db.delete_table(u'accounts_studentprofile')

        # Deleting model 'EnjazBaseProfile'
        db.delete_table(u'accounts_enjazbaseprofile')


    models = {
        u'accounts.enjazbaseprofile': {
            'Meta': {'object_name': 'EnjazBaseProfile'},
            'ar_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ar_last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ar_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'badge_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'en_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'en_last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'en_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'accounts.enjazprofile': {
            'Meta': {'object_name': 'EnjazProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'enjaz_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'accounts.nonstudentprofile': {
            'Meta': {'object_name': 'NonStudentProfile', '_ormbases': [u'accounts.EnjazBaseProfile']},
            u'enjazbaseprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.EnjazBaseProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'nonstudent_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'accounts.studentprofile': {
            'Meta': {'object_name': 'StudentProfile', '_ormbases': [u'accounts.EnjazBaseProfile']},
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clubs.College']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'enjazbaseprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.EnjazBaseProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'student_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
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
        u'clubs.college': {
            'Meta': {'object_name': 'College'},
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
        }
    }

    complete_apps = ['accounts']