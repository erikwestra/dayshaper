# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Activity', fields ['started_at']
        db.create_index(u'shared_activity', ['started_at'])

        # Adding index on 'Activity', fields ['ended_at']
        db.create_index(u'shared_activity', ['ended_at'])


    def backwards(self, orm):
        # Removing index on 'Activity', fields ['ended_at']
        db.delete_index(u'shared_activity', ['ended_at'])

        # Removing index on 'Activity', fields ['started_at']
        db.delete_index(u'shared_activity', ['started_at'])


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
            'delay_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'max_time': ('django.db.models.fields.IntegerField', [], {}),
            'min_time': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': u"orm['shared.Task']"}),
            'schedule': ('django.db.models.fields.TextField', [], {}),
            'weighting': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['shared']