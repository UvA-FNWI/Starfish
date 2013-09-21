from django.db import models
from redactor.fields import RedactorField

class Tag(models.Model):
    TAG_TYPES = (('P', 'Pedagogic'),
                 ('T', 'Tool'),
                 ('C', 'Content'),
                 ('O', 'Topic'))
    type = models.CharField(max_length=1, choices=TAG_TYPES)
    name = models.CharField(max_length=255, unique=True)
    alias_of = models.ForeignKey('Tag', null=True, blank=True)

    def __unicode__(self):
        return dict(self.TAG_TYPES)[self.type] + ":" + self.name


class Item(models.Model):
    ITEM_TYPES = (('P', 'Person'),
                  ('I', 'Info'),
                  ('Q', 'Question'))
    tags = models.ManyToManyField('Tag', blank=True)
    links = models.ManyToManyField('Item', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    type = models.CharField(max_length=1, choices=ITEM_TYPES, editable=False)
    score = models.IntegerField()


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

    full_name = models.CharField(max_length=70)
    starred = models.BooleanField(default=False)

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

    title = models.CharField(max_length=70)
    text = RedactorField(verbose_name="Text")
    authors = models.ManyToManyField(Person)

    pub_date = models.DateTimeField(auto_now=True)
    exp_date = models.DateTimeField(null=True)
    starred = models.BooleanField(default=False)
    info_type = models.CharField(max_length=2, default='IN', choices=INFO_TYPES)

    def __unicode__(self):
        return self.title


class Question(Item):
    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.type = 'Q'
    title = models.CharField(max_length=70)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

class Subscription(models.Model):
    # query ...
    pass  # FIXME
