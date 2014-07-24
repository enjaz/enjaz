# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MyProfile.last_name'
        db.delete_column(u'accounts_myprofile', 'last_name')

        # Deleting field 'MyProfile.first_name'
        db.delete_column(u'accounts_myprofile', 'first_name')

        # Adding field 'MyProfile.ar_first_name'
        db.add_column(u'accounts_myprofile', 'ar_first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.ar_middle_name'
        db.add_column(u'accounts_myprofile', 'ar_middle_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.ar_last_name'
        db.add_column(u'accounts_myprofile', 'ar_last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.en_first_name'
        db.add_column(u'accounts_myprofile', 'en_first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.en_middle_name'
        db.add_column(u'accounts_myprofile', 'en_middle_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.en_last_name'
        db.add_column(u'accounts_myprofile', 'en_last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.badge_number'
        db.add_column(u'accounts_myprofile', 'badge_number',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'MyProfile.mobile_number'
        db.add_column(u'accounts_myprofile', 'mobile_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)


        # Changing field 'MyProfile.college'
        db.alter_column(u'accounts_myprofile', 'college_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clubs.College'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):
        # Adding field 'MyProfile.last_name'
        db.add_column(u'accounts_myprofile', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'MyProfile.first_name'
        db.add_column(u'accounts_myprofile', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Deleting field 'MyProfile.ar_first_name'
        db.delete_column(u'accounts_myprofile', 'ar_first_name')

        # Deleting field 'MyProfile.ar_middle_name'
        db.delete_column(u'accounts_myprofile', 'ar_middle_name')

        # Deleting field 'MyProfile.ar_last_name'
        db.delete_column(u'accounts_myprofile', 'ar_last_name')

        # Deleting field 'MyProfile.en_first_name'
        db.delete_column(u'accounts_myprofile', 'en_first_name')

        # Deleting field 'MyProfile.en_middle_name'
        db.delete_column(u'accounts_myprofile', 'en_middle_name')

        # Deleting field 'MyProfile.en_last_name'
        db.delete_column(u'accounts_myprofile', 'en_last_name')

        # Deleting field 'MyProfile.badge_number'
        db.delete_column(u'accounts_myprofile', 'badge_number')

        # Deleting field 'MyProfile.mobile_number'
        db.delete_column(u'accounts_myprofile', 'mobile_number')


        # Changing field 'MyProfile.college'
        db.alter_column(u'accounts_myprofile', 'college_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clubs.College'], null=True))

    models = {
        u'accounts.myprofile': {
            'Meta': {'object_name': 'MyProfile'},
            'ar_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ar_last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ar_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'badge_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'college': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clubs.College']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'en_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'en_last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'en_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'student_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'enjaz_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
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
            'college_name': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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