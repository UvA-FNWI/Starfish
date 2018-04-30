# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', redactor.fields.RedactorField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('part_of', models.ForeignKey(related_name=b'subcommunities', default=None, blank=True, to='search.Community', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisplayQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=1, editable=False, choices=[(b'G', b'Good Practice'), (b'R', b'Project'), (b'E', b'Event'), (b'S', b'Glossary'), (b'I', b'Information'), (b'P', b'Person'), (b'Q', b'Question')])),
                ('score', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('searchablecontent', models.TextField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', redactor.fields.RedactorField(verbose_name=b'Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='GoodPractice',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', redactor.fields.RedactorField(verbose_name=b'Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', redactor.fields.RedactorField(verbose_name=b'Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', redactor.fields.RedactorField(verbose_name=b'Text')),
                ('date', models.DateTimeField()),
                ('location', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('handle', models.CharField(max_length=255)),
                ('title', models.CharField(default=b'', max_length=50, blank=True)),
                ('name', models.CharField(max_length=254)),
                ('headline', models.CharField(max_length=200)),
                ('about', redactor.fields.RedactorField(blank=True)),
                ('photo', models.URLField(blank=True)),
                ('website', models.URLField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True)),
                ('external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('public_email', models.BooleanField(default=True, verbose_name=b'Make email public')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', redactor.fields.RedactorField(verbose_name=b'Text')),
                ('begin_date', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name=b'+', to='search.Person', null=True)),
                ('contact', models.ForeignKey(related_name=b'+', to='search.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('item_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', redactor.fields.RedactorField(verbose_name=b'Text')),
                ('author', models.ForeignKey(related_name=b'+', to='search.Person', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stored', models.DateTimeField(auto_now=True)),
                ('persons', models.ManyToManyField(related_name=b'in_queries', null=True, to='search.Person')),
                ('result', models.ManyToManyField(related_name=b'result_of', to='search.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.ForeignKey(to='search.SearchQuery')),
                ('reader', models.ForeignKey(to='search.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[(b'P', b'Pedagogy'), (b'T', b'Technology'), (b'C', b'Content'), (b'O', b'Context/Topic')])),
                ('handle', models.CharField(unique=True, max_length=255)),
                ('alias_of', models.ForeignKey(blank=True, to='search.Tag', null=True)),
                ('glossary', models.ForeignKey(null=True, blank=True, to='search.Glossary', unique=True)),
            ],
            options={
                'ordering': ['type', 'handle'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('type', models.CharField(max_length=1, serialize=False, primary_key=True, choices=[(b'G', b'Good Practice'), (b'R', b'Project'), (b'E', b'Event'), (b'S', b'Glossary'), (b'I', b'Information'), (b'P', b'Person'), (b'Q', b'Question')])),
                ('template', redactor.fields.RedactorField(verbose_name=b'Text')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='searchquery',
            name='tags',
            field=models.ManyToManyField(related_name=b'in_queries', null=True, to='search.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='from_item',
            field=models.ForeignKey(related_name=b'+', to='search.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='to_item',
            field=models.ForeignKey(related_name=b'+', to='search.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='comments',
            field=models.ManyToManyField(to='search.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='communities',
            field=models.ManyToManyField(related_name=b'items', to='search.Community'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='links',
            field=models.ManyToManyField(to='search.Item', through='search.Link', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='search.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='information',
            name='author',
            field=models.ForeignKey(related_name=b'+', to='search.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goodpractice',
            name='author',
            field=models.ForeignKey(related_name=b'+', to='search.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='glossary',
            name='author',
            field=models.ForeignKey(related_name=b'+', to='search.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='author',
            field=models.ForeignKey(related_name=b'+', to='search.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='contact',
            field=models.ForeignKey(related_name=b'+', to='search.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='displayquery',
            name='query',
            field=models.ForeignKey(to='search.SearchQuery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='search.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='downvoters',
            field=models.ManyToManyField(related_name=b'downvoters', null=True, to='search.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='search.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='upvoters',
            field=models.ManyToManyField(related_name=b'upvoters', null=True, to='search.Person', blank=True),
            preserve_default=True,
        ),
    ]
