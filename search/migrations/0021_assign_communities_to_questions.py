# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for question in orm.Question.objects.all():
            author = question.author
            question = orm.Item.objects.get(pk=question.pk)
            if question.communities.count() == 0:
                # Determine communities based on links
                communities = set(author.communities.all())
                for link in question.links.all():
                    communities = communities.intersection(set(
                        link.communities.all()))
                for community in communities:
                    question.communities.add(community)

    def backwards(self, orm):
        "Write your backwards methods here."
        print "Cannot undo this migration"

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'search.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Person']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'downvoters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'downvoters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['search.Person']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['search.Tag']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'upvoters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'upvoters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['search.Person']"})
        },
        u'search.community': {
            'Meta': {'object_name': 'Community'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'part_of': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subcommunities'", 'null': 'True', 'blank': 'True', 'to': u"orm['search.Community']"})
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
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'text': ('redactor.fields.RedactorField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.glossary': {
            'Meta': {'object_name': 'Glossary'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['search.Person']"}),
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
            'communities': ('django.db.models.fields.related.ManyToManyField',
                [], {'default': '[1]', 'related_name': "'items'", 'symmetrical': 'False', 'to': u"orm['search.Community']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Item']", 'symmetrical': 'False', 'through': u"orm['search.Link']", 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'searchablecontent': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['search.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'search.link': {
            'Meta': {'object_name': 'Link'},
            'from_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['search.Item']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['search.Item']"})
        },
        u'search.person': {
            'Meta': {'object_name': 'Person', '_ormbases': [u'search.Item']},
            'about': ('redactor.fields.RedactorField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'item_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['search.Item']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "['type', 'handle']", 'object_name': 'Tag'},
            'alias_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Tag']", 'null': 'True', 'blank': 'True'}),
            'glossary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Glossary']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'search.template': {
            'Meta': {'object_name': 'Template'},
            'template': ('redactor.fields.RedactorField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True'})
        }
    }

    complete_apps = ['search']
    symmetrical = True
