from django.db import models
from redactor.fields import RedactorField

class Tag(models.Model):
    TAG_TYPES = (('P', 'Pedagogic'),
                 ('T', 'Tool'),
                 ('C', 'Content'),
                 ('O', 'Topic'))
    type = models.CharField(max_length=1, choices=TAG_TYPES)
    name = models.CharField(max_length=255, unique=True)
    alias_of = models.ForeignKey('self', null=True, blank=True)

    def search_format(self):
        return {'name': self.name, 'type': self.type}

    def __unicode__(self):
        return dict(self.TAG_TYPES)[self.type] + ":" + self.name

class Item(models.Model):
    ITEM_TYPES = (('P', 'Person'),
                  ('I', 'Info'),
                  ('Q', 'Question'))
    tags = models.ManyToManyField('Tag', blank=True)
    links = models.ManyToManyField('Item', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    featured = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=ITEM_TYPES, editable=False)
    score = models.IntegerField(default=0)
    searchablecontent = models.CharField(max_length=1e9, editable=False)

    def search_format(self):
        if self.type == 'P':
            return self.person.search_format()
        elif self.type == 'I':
            return self.info.search_format()
        elif self.type == 'Q':
            return self.question.search_format()
        else:
            return {
                'type':self.type,
                'tags': [t.search_format() for t in list(self.tags.all())],
                'score': self.score
            }

    def __unicode__(self):
        if self.type == 'P':
            return self.person.__unicode__()
        elif self.type == 'I':
            return self.info.__unicode__()
        elif self.type == 'Q':
            return self.question.__unicode__()
        else:
            return self.seachablecontent


class Comment(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    text = models.TextField()
    author = models.ForeignKey('Person')
    date = models.DateTimeField(auto_now=True)
    #  FIXME: Something with upvotes

    def __unicode__(self):
        return self.text[:40]


class Person(Item):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.type = 'P'
    handle = models.CharField(max_length=70)
    full_name = models.CharField(max_length=70)
    website = models.URLField(max_length=255, null=True)
    email = models.EmailField(null=True)

    def search_format(self):
        return {
            'type': 'Person',
            'id': self.id,
            'full_name': self.full_name,
            'handle': self.handle,
            'featured': self.featured,
            'score': self.score,
            'tags': [t.search_format() for t in list(self.tags.all())]
        }

    def __unicode__(self):
        return self.full_name


class Info(Item):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.type = 'I'

    INFO_TYPES = (('GP', 'Good Practice'),
                  ('IN', 'Information'),
                  ('PR', 'Project'),
                  ('EV', 'Event'))

    pub_date = models.DateTimeField(auto_now=True)
    exp_date = models.DateTimeField(null=True, blank=True)
    info_type = models.CharField(max_length=2, default='IN', choices=INFO_TYPES)
    title = models.CharField(max_length=70)
    text = RedactorField(verbose_name='Text')

    def search_format(self):
        return {
            'type': 'Info',
            'id': self.id,
            'info_type': self.info_type,
            'title': self.title,
            'featured': self.featured,
            'pub_date': self.pub_date,
            'exp_date': self.exp_date,
            'score': self.score,
            'tags': [t.search_format() for t in list(self.tags.all())]
        }

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.searchablecontent = self.title.lower() + self.text.lower()
        super(Info, self).save(*args, **kwargs)

class Question(Item):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.type = 'Q'
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=70)
    text = RedactorField(verbose_name='Text')

    def search_format(self):
        return {
            'type': 'Question',
            'id': self.id,
            'title': self.title,
            'featured': self.featured,
            'date': self.date,
            'score': self.score,
            'tags': [t.search_format() for t in list(self.tags.all())]
        }

    def save(self, *args, **kwargs):
        self.searchablecontent = self.title.lower() + self.text.lower()
        super(Question, self).save(*args, **kwargs)

class Subscription(models.Model):
    # query ...
    pass  # FIXME
