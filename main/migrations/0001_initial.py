# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Card'
        db.create_table(u'main_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'main', ['Card'])

        # Adding model 'Person'
        db.create_table(u'main_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'main', ['Person'])

        # Adding model 'CardMap'
        db.create_table(u'main_cardmap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Location'])),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Card'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Person'], null=True)),
            ('is_proxy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_foil', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['CardMap'])

        # Adding model 'Location'
        db.create_table(u'main_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Person'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'main', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Card'
        db.delete_table(u'main_card')

        # Deleting model 'Person'
        db.delete_table(u'main_person')

        # Deleting model 'CardMap'
        db.delete_table(u'main_cardmap')

        # Deleting model 'Location'
        db.delete_table(u'main_location')


    models = {
        u'main.card': {
            'Meta': {'object_name': 'Card'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'main.cardmap': {
            'Meta': {'object_name': 'CardMap'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Card']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_foil': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_proxy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Location']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Person']", 'null': 'True'})
        },
        u'main.location': {
            'Meta': {'object_name': 'Location'},
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Card']", 'through': u"orm['main.CardMap']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Person']"})
        },
        u'main.person': {
            'Meta': {'object_name': 'Person'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['main']