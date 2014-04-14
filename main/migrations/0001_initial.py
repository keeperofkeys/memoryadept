# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Set'
        db.create_table(u'main_set', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'main', ['Set'])

        # Adding model 'Type'
        db.create_table(u'main_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'main', ['Type'])

        # Adding model 'Card'
        db.create_table(u'main_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'main', ['Card'])

        # Adding M2M table for field types on 'Card'
        m2m_table_name = db.shorten_name(u'main_card_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm[u'main.card'], null=False)),
            ('type', models.ForeignKey(orm[u'main.type'], null=False))
        ))
        db.create_unique(m2m_table_name, ['card_id', 'type_id'])

        # Adding M2M table for field sets on 'Card'
        m2m_table_name = db.shorten_name(u'main_card_sets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('card', models.ForeignKey(orm[u'main.card'], null=False)),
            ('set', models.ForeignKey(orm[u'main.set'], null=False))
        ))
        db.create_unique(m2m_table_name, ['card_id', 'set_id'])

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
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Person'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'main', ['Location'])


    def backwards(self, orm):
        # Deleting model 'Set'
        db.delete_table(u'main_set')

        # Deleting model 'Type'
        db.delete_table(u'main_type')

        # Deleting model 'Card'
        db.delete_table(u'main_card')

        # Removing M2M table for field types on 'Card'
        db.delete_table(db.shorten_name(u'main_card_types'))

        # Removing M2M table for field sets on 'Card'
        db.delete_table(db.shorten_name(u'main_card_sets'))

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'sets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['main.Set']", 'null': 'True', 'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Type']", 'symmetrical': 'False', 'blank': 'True'})
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
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Card']", 'symmetrical': 'False', 'through': u"orm['main.CardMap']", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Person']"})
        },
        u'main.person': {
            'Meta': {'object_name': 'Person'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.set': {
            'Meta': {'object_name': 'Set'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'main.type': {
            'Meta': {'object_name': 'Type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['main']