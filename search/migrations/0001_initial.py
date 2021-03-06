# Generated by Django 2.0.5 on 2018-05-05 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('part_of', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcommunities', to='search.Community')),
            ],
        ),
        migrations.CreateModel(
            name='DisplayQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featured', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('G', 'Good Practice'), ('R', 'Project'), ('E', 'Event'), ('S', 'Glossary'), ('I', 'Information'), ('P', 'Person'), ('Q', 'Question')], editable=False, max_length=1)),
                ('score', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('searchablecontent', models.TextField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stored', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.SearchQuery')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('P', 'Pedagogy'), ('T', 'Technology'), ('C', 'Content'), ('O', 'Context/Topic')], max_length=1)),
                ('handle', models.CharField(max_length=255, unique=True)),
                ('alias_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.Tag')),
            ],
            options={
                'ordering': ['type', 'handle'],
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('type', models.CharField(choices=[('G', 'Good Practice'), ('R', 'Project'), ('E', 'Event'), ('S', 'Glossary'), ('I', 'Information'), ('P', 'Person'), ('Q', 'Question')], max_length=1, primary_key=True, serialize=False)),
                ('template', models.TextField(verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
                ('date', models.DateTimeField()),
                ('location', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='GoodPractice',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('handle', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, default='', max_length=50)),
                ('name', models.CharField(max_length=254)),
                ('headline', models.CharField(max_length=200)),
                ('about', models.TextField(blank=True)),
                ('photo', models.URLField(blank=True)),
                ('website', models.URLField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('external_id', models.CharField(blank=True, max_length=255, null=True)),
                ('public_email', models.BooleanField(default=True, verbose_name='Make email public')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
                ('begin_date', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='search.Person')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='search.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.Item')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(verbose_name='Text')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='search.Person')),
            ],
            options={
                'abstract': False,
            },
            bases=('search.item',),
        ),
        migrations.AddField(
            model_name='searchquery',
            name='result',
            field=models.ManyToManyField(related_name='result_of', to='search.Item'),
        ),
        migrations.AddField(
            model_name='searchquery',
            name='tags',
            field=models.ManyToManyField(related_name='in_queries', to='search.Tag'),
        ),
        migrations.AddField(
            model_name='link',
            name='from_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='search.Item'),
        ),
        migrations.AddField(
            model_name='link',
            name='to_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='search.Item'),
        ),
        migrations.AddField(
            model_name='item',
            name='comments',
            field=models.ManyToManyField(blank=True, to='search.Comment'),
        ),
        migrations.AddField(
            model_name='item',
            name='communities',
            field=models.ManyToManyField(related_name='items', to='search.Community'),
        ),
        migrations.AddField(
            model_name='item',
            name='links',
            field=models.ManyToManyField(blank=True, through='search.Link', to='search.Item'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, to='search.Tag'),
        ),
        migrations.AddField(
            model_name='displayquery',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.SearchQuery'),
        ),
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(blank=True, to='search.Tag'),
        ),
        migrations.AddField(
            model_name='tag',
            name='glossary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.Glossary', unique=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Person'),
        ),
        migrations.AddField(
            model_name='searchquery',
            name='persons',
            field=models.ManyToManyField(related_name='in_queries', to='search.Person'),
        ),
        migrations.AddField(
            model_name='information',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='search.Person'),
        ),
        migrations.AddField(
            model_name='goodpractice',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='search.Person'),
        ),
        migrations.AddField(
            model_name='glossary',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='search.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='search.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='search.Person'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Person'),
        ),
        migrations.AddField(
            model_name='comment',
            name='downvoters',
            field=models.ManyToManyField(blank=True, related_name='downvoters', to='search.Person'),
        ),
        migrations.AddField(
            model_name='comment',
            name='upvoters',
            field=models.ManyToManyField(blank=True, related_name='upvoters', to='search.Person'),
        ),
    ]
