# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def get_presidency(self, orm):
        return orm.Club.objects.get(english_name="Presidency")

    def get_media_center(self, orm):
        return orm.Club.objects.get(english_name="Media Center")

    def get_dsa(self, orm):
        return orm.Club.objects.get(english_name="Deanship of Student Affairs")

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        # Set DSA as Presidency's parent
        presidency = self.get_presidency(orm)
        presidency.parent = self.get_dsa(orm)
        presidency.save()

        # Add presidency "pseudo-clubs": Presidency Male, and Presidency Female
        male_presidency = orm.Club.objects.create(name=u"رئاسة نادي الطلاب (طلاب)",
                                english_name="Presidency (Male)",
                                description="",
                                email="sc-m@ksau-hs.edu.sa",
                                city="R",
                                visible=False,
                                can_review=True,
                                parent=self.get_presidency(orm),  # assign parent
                                )
        female_presidency = orm.Club.objects.create(name=u"رئاسة نادي الطلاب (طالبات)",
                                english_name="Presidency (Female)",
                                description="",
                                email="sc-f@ksau-hs.edu.sa",
                                city="R",
                                visible=False,
                                can_review=True,
                                parent=self.get_presidency(orm),  # assign parent
                                )

        male_pks = [3, 5, 7, 9, 10, 13, 16, 17, 18]  # Male clubs
        female_pks = [4, 6, 8, 11, 12, 14, 15, 19]  # Female clubs + Arshidni

        orm.Club.objects.filter(id__in=male_pks).update(parent=male_presidency)
        orm.Club.objects.filter(id__in=female_pks).update(parent=female_presidency)

    def backwards(self, orm):
        "Write your backwards methods here."

        # Remove presidency "pseudo-clubs"
        self.get_presidency(orm).children.delete()

        # Remove all parent-child relationships
        orm.Club.objects.all().update(parent=None)



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
        u'clubs.club': {
            'Meta': {'object_name': 'Club'},
            'can_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['clubs.Club']", 'blank': 'True', 'null': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        }
    }

    complete_apps = ['clubs']
    symmetrical = True
