# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Task.schedule'
        db.delete_column(u'shared_task', 'schedule')

        # Deleting field 'Task.delay_until'
        db.delete_column(u'shared_task', 'delay_until')

        # Adding field 'Task.enabled'
        db.add_column(u'shared_task', 'enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Task.schedule'
        db.add_column(u'shared_task', 'schedule',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Task.delay_until'
        db.add_column(u'shared_task', 'delay_until',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Deleting field 'Task.enabled'
        db.delete_column(u'shared_task', 'enabled')


    models = {
        u'shared.activity': {
            'Meta': {'object_name': 'Activity'},
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': u"orm['shared.Task']"})
        },
        u'shared.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'max_time': ('django.db.models.fields.IntegerField', [], {}),
            'min_time': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': u"orm['shared.Task']"}),
            'weighting': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['shared']