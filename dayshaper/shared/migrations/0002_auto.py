# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'shared_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activities', to=orm['shared.Task'])),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'shared', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'shared_activity')


    models = {
        u'shared.activity': {
            'Meta': {'object_name': 'Activity'},
            'ended_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': u"orm['shared.Task']"})
        },
        u'shared.task': {
            'Meta': {'object_name': 'Task'},
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