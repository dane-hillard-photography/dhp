# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table(u'photography_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='3a548b20-7347-49d7-8c09-a9e403d1eb8d', unique=True, max_length=36)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=2, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'photography', ['Album'])

        # Adding model 'Tag'
        db.create_table(u'photography_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'photography', ['Tag'])

        # Adding model 'Photograph'
        db.create_table(u'photography_photograph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('orientation', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='91a20bed-f56c-4fcb-9e40-6211127dd8d8', unique=True, max_length=36)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('l_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('l_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('m_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('m_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sm_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sm_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sq_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sq_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('thumbnail_large', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail_medium', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail_small', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('thumbnail_square', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'photography', ['Photograph'])

        # Adding M2M table for field albums on 'Photograph'
        m2m_table_name = db.shorten_name(u'photography_photograph_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photograph', models.ForeignKey(orm[u'photography.photograph'], null=False)),
            ('album', models.ForeignKey(orm[u'photography.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photograph_id', 'album_id'])

        # Adding M2M table for field tags on 'Photograph'
        m2m_table_name = db.shorten_name(u'photography_photograph_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photograph', models.ForeignKey(orm[u'photography.photograph'], null=False)),
            ('tag', models.ForeignKey(orm[u'photography.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['photograph_id', 'tag_id'])

        # Adding model 'Service'
        db.create_table(u'photography_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'photography', ['Service'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'photography_album')

        # Deleting model 'Tag'
        db.delete_table(u'photography_tag')

        # Deleting model 'Photograph'
        db.delete_table(u'photography_photograph')

        # Removing M2M table for field albums on 'Photograph'
        db.delete_table(db.shorten_name(u'photography_photograph_albums'))

        # Removing M2M table for field tags on 'Photograph'
        db.delete_table(db.shorten_name(u'photography_photograph_tags'))

        # Deleting model 'Service'
        db.delete_table(u'photography_service')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'photography.album': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Album'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'625ef950-cd8a-4287-9343-353ba4fdb19f'", 'unique': 'True', 'max_length': '36'})
        },
        u'photography.photograph': {
            'Meta': {'ordering': "['-published_date']", 'object_name': 'Photograph'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['photography.Album']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'l_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'l_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'm_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'm_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orientation': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sm_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sm_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sq_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sq_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['photography.Tag']", 'symmetrical': 'False'}),
            'thumbnail_large': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_medium': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'thumbnail_square': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'69ef1d80-08a5-467c-9270-084040b91325'", 'unique': 'True', 'max_length': '36'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'photography.service': {
            'Meta': {'object_name': 'Service'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'photography.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['photography']