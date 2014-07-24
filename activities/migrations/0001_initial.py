# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'activities_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_club', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_activity', null=True, on_delete=models.SET_NULL, to=orm['clubs.Club'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('requirements', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('collect_participants', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inside_collaborators', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('outside_collaborators', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('participants', self.gf('django.db.models.fields.IntegerField')()),
            ('organizers', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'activities', ['Activity'])

        # Adding M2M table for field secondary_clubs on 'Activity'
        m2m_table_name = db.shorten_name(u'activities_activity_secondary_clubs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'activities.activity'], null=False)),
            ('club', models.ForeignKey(orm[u'clubs.club'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'club_id'])

        # Adding M2M table for field participant_colleges on 'Activity'
        m2m_table_name = db.shorten_name(u'activities_activity_participant_colleges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'activities.activity'], null=False)),
            ('college', models.ForeignKey(orm[u'clubs.college'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'college_id'])

        # Adding model 'Review'
        db.create_table(u'activities_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Activity'])),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('review_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('clubs_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('datetime_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('requirement_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('inside_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('outside_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('participants_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('organizers_notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('review_type', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('is_approved', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'activities', ['Review'])

        # Adding model 'Participation'
        db.create_table(u'activities_participation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Activity'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'activities', ['Participation'])

        # Adding model 'Episode'
        db.create_table(u'activities_episode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Activity'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'activities', ['Episode'])


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'activities_activity')

        # Removing M2M table for field secondary_clubs on 'Activity'
        db.delete_table(db.shorten_name(u'activities_activity_secondary_clubs'))

        # Removing M2M table for field participant_colleges on 'Activity'
        db.delete_table(db.shorten_name(u'activities_activity_participant_colleges'))

        # Deleting model 'Review'
        db.delete_table(u'activities_review')

        # Deleting model 'Participation'
        db.delete_table(u'activities_participation')

        # Deleting model 'Episode'
        db.delete_table(u'activities_episode')


    models = {
        u'activities.activity': {
            'Meta': {'object_name': 'Activity'},
            'collect_participants': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inside_collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organizers': ('django.db.models.fields.IntegerField', [], {}),
            'outside_collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'participant_colleges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['clubs.College']", 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.IntegerField', [], {}),
            'primary_club': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_activity'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['clubs.Club']"}),
            'requirements': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secondary_clubs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_activity'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['clubs.Club']"}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        u'activities.episode': {
            'Meta': {'object_name': 'Episode'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'activities.participation': {
            'Meta': {'object_name': 'Participation'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        u'activities.review': {
            'Meta': {'object_name': 'Review'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            'clubs_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'datetime_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inside_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_approved': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organizers_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'outside_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'participants_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'requirement_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'review_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'review_type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
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
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'coordination'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'english_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'open_membership': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parenthood'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['clubs.Club']", 'blank': 'True', 'null': 'True'})
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

    complete_apps = ['activities']