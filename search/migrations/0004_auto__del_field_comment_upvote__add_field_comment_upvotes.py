# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Comment.upvote'
        db.delete_column(u'search_comment', 'upvote')

        # Adding field 'Comment.upvotes'
        db.add_column(u'search_comment', 'upvotes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field voters on 'Comment'
        m2m_table_name = db.shorten_name(u'search_comment_voters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'search.comment'], null=False)),
            ('person', models.ForeignKey(orm[u'search.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'person_id'])


    def backwards(self, orm):
        # Adding field 'Comment.upvote'
        db.add_column(u'search_comment', 'upvote',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Comment.upvotes'
        db.delete_column(u'search_comment', 'upvotes')

        # Removing M2M table for field voters on 'Comment'
        db.delete_table(db.shorten_name(u'search_comment_voters'))


    models = {
        u'search.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Person']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'voters'", 'symmetrical': 'False', 'to': u"orm['search.Person']"})
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
            'about': ('redactor.fields.RedactorField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '254', 'blank': 'True'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
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