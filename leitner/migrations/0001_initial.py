# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Face'
        db.create_table('leitner_face', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageWithThumbnailsField')(max_length=100, blank=True)),
            ('tex', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('leitner', ['Face'])

        # Adding model 'Card'
        db.create_table('leitner_card', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('front', self.gf('django.db.models.fields.related.ForeignKey')(related_name='front', to=orm['leitner.Face'])),
            ('back', self.gf('django.db.models.fields.related.ForeignKey')(related_name='back', to=orm['leitner.Face'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('leitner', ['Card'])

        # Adding model 'Deck'
        db.create_table('leitner_deck', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('leitner', ['Deck'])

        # Adding model 'DeckCard'
        db.create_table('leitner_deckcard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deck', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leitner.Deck'])),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leitner.Card'])),
        ))
        db.send_create_signal('leitner', ['DeckCard'])

        # Adding model 'UserCard'
        db.create_table('leitner_usercard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leitner.Card'])),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('due', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('rung', self.gf('django.db.models.fields.SmallIntegerField')(default=-1)),
            ('ease', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5)),
        ))
        db.send_create_signal('leitner', ['UserCard'])

        # Adding model 'UserCardTest'
        db.create_table('leitner_usercardtest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usercard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leitner.UserCard'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('old_rung', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('new_rung', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('leitner', ['UserCardTest'])


    def backwards(self, orm):
        
        # Deleting model 'Face'
        db.delete_table('leitner_face')

        # Deleting model 'Card'
        db.delete_table('leitner_card')

        # Deleting model 'Deck'
        db.delete_table('leitner_deck')

        # Deleting model 'DeckCard'
        db.delete_table('leitner_deckcard')

        # Deleting model 'UserCard'
        db.delete_table('leitner_usercard')

        # Deleting model 'UserCardTest'
        db.delete_table('leitner_usercardtest')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'leitner.card': {
            'Meta': {'object_name': 'Card'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'back': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'back'", 'to': "orm['leitner.Face']"}),
            'front': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'front'", 'to': "orm['leitner.Face']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'leitner.deck': {
            'Meta': {'object_name': 'Deck'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'leitner.deckcard': {
            'Meta': {'object_name': 'DeckCard'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['leitner.Card']"}),
            'deck': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['leitner.Deck']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'leitner.face': {
            'Meta': {'object_name': 'Face'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageWithThumbnailsField', [], {'max_length': '100', 'blank': 'True'}),
            'tex': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        'leitner.usercard': {
            'Meta': {'object_name': 'UserCard'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['leitner.Card']"}),
            'due': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'ease': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'rung': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'leitner.usercardtest': {
            'Meta': {'object_name': 'UserCardTest'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_rung': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'old_rung': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'usercard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['leitner.UserCard']"})
        }
    }

    complete_apps = ['leitner']
