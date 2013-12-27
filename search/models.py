from django.db import models
from redactor.fields import RedactorField
from HTMLParser import HTMLParser
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ' '.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class Tag(models.Model):
    TAG_TYPES = (('P', 'Pedagogy'),
                 ('T', 'Technology'),
                 ('C', 'Content'),
                 ('O', 'Topic'))
    # The type of this tag, used for coloring
    type = models.CharField(max_length=1, choices=TAG_TYPES)
    # The handle by which this tag will be identified
    handle = models.CharField(max_length=255, unique=True)
    # The glossary item that explains the tag
    glossary = models.ForeignKey('Glossary', null=True, blank=True)
    # The reference to the Tag of which this is an alias (if applicable)
    alias_of = models.ForeignKey('self', null=True, blank=True)

    def dict_format(self):
        """representation used to communicate the model to the client."""
        alias_of_handle = None
        if self.alias_of:
            alias_of_handle = self.alias_of.handle
        info_dict = None
        if self.glossary:
            info_dict = {'title': self.glossary.title,
                         'text': self.glossary.text,
                         'author': self.glossary.author,
                         'summary': self.glossary.summary(max_len=480)}
        return {'handle': self.handle,
                'type': self.type,
                'type_name': dict(self.TAG_TYPES)[self.type],
                'alias_of': alias_of_handle,
                'glossary': info_dict,
                'get_absolute_url': self.get_absolute_url()}

    def __unicode__(self):
        s = dict(self.TAG_TYPES)[self.type] + ":" + self.handle
        if self.alias_of:
            s += ' > ' + self.alias_of.handle
        return s

    def get_absolute_url(self):
        return '/tag/' + str(self.handle)

    class Meta:
        ordering = ['type', 'handle']


class Item(models.Model):
    # Types of items
    ITEM_TYPES = (('P', 'Person'),
                  ('G', 'Good Practice'),
                  ('I', 'Information'),
                  ('R', 'Project'),
                  ('E', 'Event'),
                  ('Q', 'Question'),
                  ('S', 'Glossary'))
    # Tags linked to this item
    tags = models.ManyToManyField('Tag', blank=True)
    # The other items that are linked to this item
    links = models.ManyToManyField('Item', blank=True)
    # The comments linked to this item
    comments = models.ManyToManyField('Comment', blank=True, editable=False)
    # Whether this item is featured by a moderator
    featured = models.BooleanField(default=False)
    # The type of this item, important to know which subclass to load
    type = models.CharField(max_length=1, choices=ITEM_TYPES, editable=False)
    # The score of this item, which can be used for ranking of search results
    score = models.IntegerField(default=0)
    # The date that this item was created in the database
    create_date = models.DateTimeField(auto_now=True, editable=False)
    # The concatenated string representation of each item for free text search
    searchablecontent = models.TextField(editable=False)

    # Return reference the proper subclass when possible, else return None
    def downcast(self):
        # Define links to subclasses
        subcls = {
            'P': lambda self: self.person,
            'G': lambda self: self.goodpractice,
            'I': lambda self: self.information,
            'R': lambda self: self.project,
            'E': lambda self: self.event,
            'Q': lambda self: self.question,
            'S': lambda self: self.glossary
        }
        # If link to the current subclass is known
        if self.type in subcls:
            return subcls[self.type](self)
        else:
            return None

    def summary(self):
        return ""

    def _truncate(self, text, max_len=200):
        if len(text) > max_len:
            return strip_tags(text)[:max_len - 2] + "..."
        return strip_tags(text)

    # Dictionary representation used to communicate the model to the client
    def dict_format(self, obj={}):
        # Fill dict format at this level
        # make sure the pass by reference does not cause unexpected results
        obj = obj.copy()
        obj.update({
            'id': self.id,
            'type': dict(self.ITEM_TYPES)[self.type],
            'tags': [t.dict_format() for t in list(self.tags.all())],
            'featured': self.featured,
            'score': self.score,
            'summary': self.summary(),
            'create_date': self.create_date,
            'get_absolute_url': self.downcast().get_absolute_url()
        })
        # Attempt to get reference to subclass
        subcls = self.downcast()
        # Attempt to let subclasses fill in dict format further
        if subcls is not None and hasattr(subcls, 'dict_format'):
            return subcls.dict_format(obj)
        else:
            return obj

    def get_absolute_url(self):
        if self.type in dict(self.ITEM_TYPES):
            t = dict(self.ITEM_TYPES)[self.type].lower().replace(" ", "")
            return '/' + t + "/" + str(self.id)
        else:
            return '/item/' + str(self.id)

    def __unicode__(self):
        # Attempt to get reference to subclass
        subcls = self.downcast()
        if subcls is not None:
            return subcls.__unicode__()
        else:
            return self.searchablecontent[:40]


class Comment(models.Model):
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    text = models.TextField()
    author = models.ForeignKey('Person')
    date = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    voters = models.ManyToManyField('Person', related_name='voters', blank=True, null=True)

    def __unicode__(self):
        return self.text[:40]

    def summary(self):
        return self._truncate(self.text)


class Person(Item):
    # Handle to identify this person with
    handle = models.CharField(max_length=255)
    # The official title, e.g. `dr.' or `prof.'
    title = models.CharField(max_length=50, blank=True, default="")
    # The full name of this person, including first names and family name
    name = models.CharField(max_length=254)
    # Short text describing the core of this person
    headline = models.CharField(max_length=200)
    # Text describing this person
    about = RedactorField(blank=True)
    # The source of a photo
    photo = models.URLField(blank=True)
    # The website of this person
    website = models.URLField(max_length=255, null=True, blank=True)
    # The email address of this person
    email = models.EmailField(null=True)
    # User corresponding to this person. If user deleted, person remains.
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
            blank=True)

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.type = 'P'

    def summary(self):
        return self.headline

    def dict_format(self, obj=None):
        """Dictionary representation used to communicate the model to the
        client.
        """
        if obj is None:
            return super(Person, self).dict_format()
        else:
            obj.update({
                'handle': self.handle,
                'title': self.title,
                'name': self.name,
                'about': self.about,
                'photo': self.photo,
                'website': self.website,
                'summary': self.summary(),
                'email': self.email,
            })
            return obj

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.searchablecontent = ' '.join([self.name.lower(),
                                           self.about.lower(),
                                           self.headline.lower()])
        super(Person, self).save(*args, **kwargs)


class TextItem(Item):
    # The title of the good practice
    title = models.CharField(max_length=255)
    # The WYSIWYG text of the good practice
    text = RedactorField(verbose_name='Text')
    # The person who created the good practice
    author = models.ForeignKey('Person', null=True, related_name='+')

    class Meta:
        abstract = True

    def summary(self, max_len=200):
        return self._truncate(self.text, max_len=max_len)

    def dict_format(self, obj=None):
        """Dictionary representation used to communicate the model to the
        client.
        """
        if obj is None:
            return super(self.__class__, self).dict_format()
        else:
            # make sure the pass by reference does not cause unexpected results
            obj = obj.copy()
            obj.update({
                'author': self.author.dict_format(),
                'title': self.title,
                'summary': self.summary(),
                'text': self.text
            })
            return obj

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.searchablecontent = self.title.lower() + ' ' + self.text.lower()
        super(TextItem, self).save(*args, **kwargs)


class GoodPractice(TextItem):
    def __init__(self, *args, **kwargs):
        super(GoodPractice, self).__init__(*args, **kwargs)
        self.type = 'G'


class Information(TextItem):
    def __init__(self, *args, **kwargs):
        super(Information, self).__init__(*args, **kwargs)
        self.type = 'I'

class Project(TextItem):
    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.type = 'R'

    # The person who can be contacted for more info on the project
    contact = models.ForeignKey('Person', related_name='+')
    # The begin date of the project
    begin_date = models.DateTimeField(auto_now=True, editable=True)
    # The end date of the project
    end_date = models.DateTimeField(auto_now=True, editable=True)

    def dict_format(self, obj=None):
        """Dictionary representation used to communicate the model to the
        client.
        """
        if obj is None:
            return super(Project, self).dict_format()
        else:
            # make sure the pass by reference does not cause unexpected results
            obj = obj.copy()
            obj.update({
                'author': self.author,
                'title': self.title,
                'text': self.text,
                'summary': self.summary(),
                'contact': self.contact.dict_format(),
                'begin_date': self.begin_date,
                'end_date': self.end_date
            })
            return obj


class Event(TextItem):
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.type = 'E'

    # The person who can be contacted for more info on the project
    contact = models.ForeignKey('Person', related_name='+')
    # The date of the event
    date = models.DateTimeField(editable=True)
    location = models.CharField(max_length=255, blank=True, default="")

    @property
    def is_past_due(self):
        t = timezone.make_aware(datetime.now(),
                                timezone.get_default_timezone())
        if t > self.date:
            return True
        return False

    def dict_format(self, obj=None):
        """Dictionary representation used to communicate the model to the
        client.
        """
        if obj is None:
            return super(Event, self).dict_format()
        else:
            obj.update({
                'author': self.author,
                'title': self.title,
                'text': self.text,
                'is_past_due': self.is_past_due,
                'location': self.location,
                'summary': self.summary(),
                'contact': self.contact.dict_format(),
                'date': self.date
            })
            return obj


class Question(TextItem):
    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)
        self.type = 'Q'

    def __unicode__(self):
        return self.title


class Glossary(TextItem):
    def __init__(self, *args, **kwargs):
        super(Glossary, self).__init__(*args, **kwargs)
        self.type = 'S'


# Queries can be stored to either be displayed on the main page, rss feed or to
# allow persons to subscribe to the query in order to be notified if the
# results are updated (i.e. new results can be found).
class SearchQuery(models.Model):
    # Which tags are mentioned in the query
    tags = models.ManyToManyField(Tag, null=True, related_name='in_queries')
    # Which persons are mentioned in the query
    persons = models.ManyToManyField(Person, null=True,
                                     related_name='in_queries')
    # What was the last known (cached) result of this query
    result = models.ManyToManyField(Item, related_name='result_of')
    # When was the query stored
    stored = models.DateTimeField(auto_now=True)


# Subscriptions indicate to update the reader if results of a query change
class Subscription(models.Model):
    # What query is subscribed to?
    query = models.ForeignKey(SearchQuery, null=False)
    # Who is subscribing to this query (to contact this person later)
    reader = models.ForeignKey(Person, null=False)


# DisplayQueries indicate to show the query on the homepage
class DisplayQuery(models.Model):
    # The query that is displayed
    query = models.ForeignKey(SearchQuery, null=False)
    # The template to use when rendering
    template = models.CharField(max_length=100)
