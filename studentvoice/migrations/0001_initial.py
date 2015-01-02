# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Voice'
        db.create_table(u'studentvoice_voice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('solution', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['studentvoice.Recipient'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('was_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_published', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('is_editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('number_of_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('number_of_comments', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='replies', null=True, on_delete=models.SET_NULL, to=orm['studentvoice.Voice'])),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'studentvoice', ['Voice'])

        # Adding model 'Vote'
        db.create_table(u'studentvoice_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('voice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['studentvoice.Voice'], null=True, on_delete=models.SET_NULL)),
            ('is_counted', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('vote_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'studentvoice', ['Vote'])

        # Adding model 'Response'
        db.create_table(u'studentvoice_response', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('voice', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['studentvoice.Voice'], unique=True, null=True, on_delete=models.SET_NULL)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'studentvoice', ['Response'])

        # Adding model 'View'
        db.create_table(u'studentvoice_view', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('viewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('is_counted', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('voice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['studentvoice.Voice'], null=True, on_delete=models.SET_NULL)),
            ('view_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'studentvoice', ['View'])

        # Adding model 'Recipient'
        db.create_table(u'studentvoice_recipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('english_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('secondary_email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'studentvoice', ['Recipient'])

        # Adding M2M table for field college on 'Recipient'
        m2m_table_name = db.shorten_name(u'studentvoice_recipient_college')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipient', models.ForeignKey(orm[u'studentvoice.recipient'], null=False)),
            ('college', models.ForeignKey(orm[u'clubs.college'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipient_id', 'college_id'])

        # Adding M2M table for field users on 'Recipient'
        m2m_table_name = db.shorten_name(u'studentvoice_recipient_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipient', models.ForeignKey(orm[u'studentvoice.recipient'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['recipient_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Voice'
        db.delete_table(u'studentvoice_voice')

        # Deleting model 'Vote'
        db.delete_table(u'studentvoice_vote')

        # Deleting model 'Response'
        db.delete_table(u'studentvoice_response')

        # Deleting model 'View'
        db.delete_table(u'studentvoice_view')

        # Deleting model 'Recipient'
        db.delete_table(u'studentvoice_recipient')

        # Removing M2M table for field college on 'Recipient'
        db.delete_table(db.shorten_name(u'studentvoice_recipient_college'))

        # Removing M2M table for field users on 'Recipient'
        db.delete_table(db.shorten_name(u'studentvoice_recipient_users'))


    models = {
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
        u'studentvoice.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'college': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['clubs.College']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'english_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'studentvoice.response': {
            'Meta': {'object_name': 'Response'},
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'voice': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['studentvoice.Voice']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        u'studentvoice.view': {
            'Meta': {'object_name': 'View'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_counted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'view_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'voice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentvoice.Voice']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        u'studentvoice.voice': {
            'Meta': {'object_name': 'Voice'},
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_published': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'number_of_comments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_of_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['studentvoice.Voice']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentvoice.Recipient']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'solution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'was_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'studentvoice.vote': {
            'Meta': {'object_name': 'Vote'},
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_counted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'voice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['studentvoice.Voice']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'vote_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['studentvoice']