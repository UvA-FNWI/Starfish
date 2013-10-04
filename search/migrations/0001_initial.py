# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'search_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('handle', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Information'], null=True, blank=True)),
            ('alias_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Tag'], null=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['Tag'])

        # Adding model 'Item'
        db.create_table(u'search_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('searchablecontent', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'search', ['Item'])

        # Adding M2M table for field tags on 'Item'
        m2m_table_name = db.shorten_name(u'search_item_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'search.item'], null=False)),
            ('tag', models.ForeignKey(orm[u'search.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'tag_id'])

        # Adding M2M table for field links on 'Item'
        m2m_table_name = db.shorten_name(u'search_item_links')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_item', models.ForeignKey(orm[u'search.item'], null=False)),
            ('to_item', models.ForeignKey(orm[u'search.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_item_id', 'to_item_id'])

        # Adding M2M table for field comments on 'Item'
        m2m_table_name = db.shorten_name(u'search_item_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'search.item'], null=False)),
            ('comment', models.ForeignKey(orm[u'search.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'comment_id'])

        # Adding model 'Comment'
        db.create_table(u'search_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Person'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['Comment'])

        # Adding M2M table for field tags on 'Comment'
        m2m_table_name = db.shorten_name(u'search_comment_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'search.comment'], null=False)),
            ('tag', models.ForeignKey(orm[u'search.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'tag_id'])

        # Adding model 'Person'
        db.create_table(u'search_person', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['search.Item'], unique=True, primary_key=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('about', self.gf('redactor.fields.RedactorField')()),
            ('photo', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=255, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
        ))
        db.send_create_signal(u'search', ['Person'])

        # Adding model 'GoodPractice'
        db.create_table(u'search_goodpractice', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['search.Item'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('redactor.fields.RedactorField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['search.Person'])),
        ))
        db.send_create_signal(u'search', ['GoodPractice'])

        # Adding model 'Information'
        db.create_table(u'search_information', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['search.Item'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('redactor.fields.RedactorField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['search.Person'])),
        ))
        db.send_create_signal(u'search', ['Information'])

        # Adding model 'Project'
        db.create_table(u'search_project', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['search.Item'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('redactor.fields.RedactorField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['search.Person'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['search.Person'])),
            ('begin_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['Project'])

        # Adding model 'Event'
        db.create_table(u'search_event', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['search.Item'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('redactor.fields.RedactorField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['search.Person'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['search.Person'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['Event'])

        # Adding model 'Question'
        db.create_table(u'search_question', (
            (u'item_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['search.Item'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('redactor.fields.RedactorField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['search.Person'])),
        ))
        db.send_create_signal(u'search', ['Question'])

        # Adding model 'SearchQuery'
        db.create_table(u'search_searchquery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stored', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['SearchQuery'])

        # Adding M2M table for field tags on 'SearchQuery'
        m2m_table_name = db.shorten_name(u'search_searchquery_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('searchquery', models.ForeignKey(orm[u'search.searchquery'], null=False)),
            ('tag', models.ForeignKey(orm[u'search.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['searchquery_id', 'tag_id'])

        # Adding M2M table for field persons on 'SearchQuery'
        m2m_table_name = db.shorten_name(u'search_searchquery_persons')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('searchquery', models.ForeignKey(orm[u'search.searchquery'], null=False)),
            ('person', models.ForeignKey(orm[u'search.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['searchquery_id', 'person_id'])

        # Adding M2M table for field result on 'SearchQuery'
        m2m_table_name = db.shorten_name(u'search_searchquery_result')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('searchquery', models.ForeignKey(orm[u'search.searchquery'], null=False)),
            ('item', models.ForeignKey(orm[u'search.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['searchquery_id', 'item_id'])

        # Adding model 'Subscription'
        db.create_table(u'search_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.SearchQuery'])),
            ('reader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Person'])),
        ))
        db.send_create_signal(u'search', ['Subscription'])

        # Adding model 'DisplayQuery'
        db.create_table(u'search_displayquery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.SearchQuery'])),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'search', ['DisplayQuery'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'search_tag')

        # Deleting model 'Item'
        db.delete_table(u'search_item')

        # Removing M2M table for field tags on 'Item'
        db.delete_table(db.shorten_name(u'search_item_tags'))

        # Removing M2M table for field links on 'Item'
        db.delete_table(db.shorten_name(u'search_item_links'))

        # Removing M2M table for field comments on 'Item'
        db.delete_table(db.shorten_name(u'search_item_comments'))

        # Deleting model 'Comment'
        db.delete_table(u'search_comment')

        # Removing M2M table for field tags on 'Comment'
        db.delete_table(db.shorten_name(u'search_comment_tags'))

        # Deleting model 'Person'
        db.delete_table(u'search_person')

        # Deleting model 'GoodPractice'
        db.delete_table(u'search_goodpractice')

        # Deleting model 'Information'
        db.delete_table(u'search_information')

        # Deleting model 'Project'
        db.delete_table(u'search_project')

        # Deleting model 'Event'
        db.delete_table(u'search_event')

        # Deleting model 'Question'
        db.delete_table(u'search_question')

        # Deleting model 'SearchQuery'
        db.delete_table(u'search_searchquery')

        # Removing M2M table for field tags on 'SearchQuery'
        db.delete_table(db.shorten_name(u'search_searchquery_tags'))

        # Removing M2M table for field persons on 'SearchQuery'
        db.delete_table(db.shorten_name(u'search_searchquery_persons'))

        # Removing M2M table for field result on 'SearchQuery'
        db.delete_table(db.shorten_name(u'search_searchquery_result'))

        # Deleting model 'Subscription'
        db.delete_table(u'search_subscription')

        # Deleting model 'DisplayQuery'
        db.delete_table(u'search_displayquery')


    models = {
        u'search.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Person']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'search.displayquery': {
            'Meta': {'object_name': 'DisplayQuery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.SearchQuery']"}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'search.event': {
            'Meta': {'object_name': 'Event'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['search.Person']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['search.Person']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.goodpractice': {
            'Meta': {'object_name': 'GoodPractice'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['search.Person']"}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.information': {
            'Meta': {'object_name': 'Information'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['search.Person']"}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.item': {
            'Meta': {'object_name': 'Item'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Comment']", 'symmetrical': 'False', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Item']", 'symmetrical': 'False', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'searchablecontent': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'search.person': {
            'Meta': {'object_name': 'Person', '_ormbases': [u'search.Item']},
            'about': ('redactor.fields.RedactorField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True'})
        },
        u'search.project': {
            'Meta': {'object_name': 'Project'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['search.Person']"}),
            'begin_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['search.Person']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.question': {
            'Meta': {'object_name': 'Question'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['search.Person']"}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.searchquery': {
            'Meta': {'object_name': 'SearchQuery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'in_queries'", 'null': 'True', 'to': u"orm['search.Person']"}),
            'result': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'result_of'", 'symmetrical': 'False', 'to': u"orm['search.Item']"}),
            'stored': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'in_queries'", 'null': 'True', 'to': u"orm['search.Tag']"})
        },
        u'search.subscription': {
            'Meta': {'object_name': 'Subscription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.SearchQuery']"}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Person']"})
        },
        u'search.tag': {
            'Meta': {'object_name': 'Tag'},
            'alias_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Tag']", 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Information']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['search']