# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'shared_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shared.Task'], null=True)),
            ('label', self.gf('django.db.models.fields.TextField')()),
            ('weighting', self.gf('django.db.models.fields.FloatField')()),
            ('min_time', self.gf('django.db.models.fields.IntegerField')()),
            ('max_time', self.gf('django.db.models.fields.IntegerField')()),
            ('schedule', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'shared', ['Task'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'shared_task')


    models = {
        u'shared.task': {
            'Meta': {'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'max_time': ('django.db.models.fields.IntegerField', [], {}),
            'min_time': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shared.Task']", 'null': 'True'}),
            'schedule': ('django.db.models.fields.TextField', [], {}),
            'weighting': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['shared']