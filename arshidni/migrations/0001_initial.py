# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArshidniProfile'
        db.create_table(u'arshidni_arshidniprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interests', self.gf('django.db.models.fields.TextField')()),
            ('contacts', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_published', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['ArshidniProfile'])

        # Adding model 'GraduateProfile'
        db.create_table(u'arshidni_graduateprofile', (
            (u'arshidniprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['arshidni.ArshidniProfile'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='graduate_profile', unique=True, null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('answers_questions', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('gives_lectures', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'arshidni', ['GraduateProfile'])

        # Adding model 'Question'
        db.create_table(u'arshidni_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('college', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('is_published', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('is_answered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'arshidni_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['arshidni.Question'], null=True, on_delete=models.SET_NULL)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['arshidni.Answer'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('is_editable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['Answer'])

        # Adding model 'StudyGroup'
        db.create_table(u'arshidni_studygroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coordinator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='studygroup_coordination', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('starting_date', self.gf('django.db.models.fields.DateField')()),
            ('ending_date', self.gf('django.db.models.fields.DateField')()),
            ('max_members', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('is_published', self.gf('django.db.models.fields.NullBooleanField')(default=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['StudyGroup'])

        # Adding M2M table for field members on 'StudyGroup'
        m2m_table_name = db.shorten_name(u'arshidni_studygroup_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studygroup', models.ForeignKey(orm[u'arshidni.studygroup'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['studygroup_id', 'user_id'])

        # Adding model 'LearningObjective'
        db.create_table(u'arshidni_learningobjective', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['arshidni.StudyGroup'], null=True, on_delete=models.SET_NULL)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['LearningObjective'])

        # Adding model 'JoinStudyGroupRequest'
        db.create_table(u'arshidni_joinstudygrouprequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.SET_NULL)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='join_requests', null=True, on_delete=models.SET_NULL, to=orm['arshidni.StudyGroup'])),
            ('is_accepted', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['JoinStudyGroupRequest'])

        # Adding model 'ColleagueProfile'
        db.create_table(u'arshidni_colleagueprofile', (
            (u'arshidniprofile_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['arshidni.ArshidniProfile'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='colleague_profile', unique=True, null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('batch', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'arshidni', ['ColleagueProfile'])

        # Adding model 'SupervisionRequest'
        db.create_table(u'arshidni_supervisionrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supervision_requests', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('colleague', self.gf('django.db.models.fields.related.ForeignKey')(related_name='colleague', null=True, on_delete=models.SET_NULL, to=orm['arshidni.ColleagueProfile'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=2)),
            ('contacts', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('interests', self.gf('django.db.models.fields.TextField')()),
            ('batch', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('withdrawal_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'arshidni', ['SupervisionRequest'])


    def backwards(self, orm):
        # Deleting model 'ArshidniProfile'
        db.delete_table(u'arshidni_arshidniprofile')

        # Deleting model 'GraduateProfile'
        db.delete_table(u'arshidni_graduateprofile')

        # Deleting model 'Question'
        db.delete_table(u'arshidni_question')

        # Deleting model 'Answer'
        db.delete_table(u'arshidni_answer')

        # Deleting model 'StudyGroup'
        db.delete_table(u'arshidni_studygroup')

        # Removing M2M table for field members on 'StudyGroup'
        db.delete_table(db.shorten_name(u'arshidni_studygroup_members'))

        # Deleting model 'LearningObjective'
        db.delete_table(u'arshidni_learningobjective')

        # Deleting model 'JoinStudyGroupRequest'
        db.delete_table(u'arshidni_joinstudygrouprequest')

        # Deleting model 'ColleagueProfile'
        db.delete_table(u'arshidni_colleagueprofile')

        # Deleting model 'SupervisionRequest'
        db.delete_table(u'arshidni_supervisionrequest')


    models = {
        u'arshidni.answer': {
            'Meta': {'object_name': 'Answer'},
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_published': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['arshidni.Answer']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['arshidni.Question']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'arshidni.arshidniprofile': {
            'Meta': {'object_name': 'ArshidniProfile'},
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {}),
            'is_published': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'arshidni.colleagueprofile': {
            'Meta': {'object_name': 'ColleagueProfile', '_ormbases': [u'arshidni.ArshidniProfile']},
            u'arshidniprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['arshidni.ArshidniProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'batch': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'bio': ('django.db.models.fields.TextField', [], {}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'colleague_profile'", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'arshidni.graduateprofile': {
            'Meta': {'object_name': 'GraduateProfile', '_ormbases': [u'arshidni.ArshidniProfile']},
            'answers_questions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'arshidniprofile_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['arshidni.ArshidniProfile']", 'unique': 'True', 'primary_key': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {}),
            'gives_lectures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'graduate_profile'", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'arshidni.joinstudygrouprequest': {
            'Meta': {'object_name': 'JoinStudyGroupRequest'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'join_requests'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['arshidni.StudyGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'})
        },
        u'arshidni.learningobjective': {
            'Meta': {'object_name': 'LearningObjective'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['arshidni.StudyGroup']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'arshidni.question': {
            'Meta': {'object_name': 'Question'},
            'college': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_answered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_published': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'arshidni.studygroup': {
            'Meta': {'object_name': 'StudyGroup'},
            'coordinator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'studygroup_coordination'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ending_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'max_members': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'studygroup_memberships'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'starting_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'arshidni.supervisionrequest': {
            'Meta': {'object_name': 'SupervisionRequest'},
            'batch': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'colleague': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'colleague'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['arshidni.ColleagueProfile']"}),
            'contacts': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supervision_requests'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'withdrawal_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['arshidni']