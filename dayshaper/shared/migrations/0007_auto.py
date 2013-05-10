# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.strategy'
        db.add_column(u'shared_task', 'strategy',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.strategy'
        db.delete_column(u'shared_task', 'strategy')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'max_time': ('django.db.models.fields.IntegerField', [], {}),
            'min_time': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': u"orm['shared.Task']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'strategy': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'weighting': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['shared']