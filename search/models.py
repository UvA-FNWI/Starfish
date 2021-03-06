from django.db import models
from html.parser import HTMLParser
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import ckeditor_uploader.fields as ck_field
import re

ITEM_TYPES = settings.ITEM_TYPES

def get_template(item):
    if item == GoodPractice:
        item = 'G'
    elif item == Project:
        item = 'R'
    elif item == Information:
        item = 'I'
    elif item == Event:
        item = 'E'
    elif item == Person:
        item = 'P'
    elif item == Glossary:
        item = 'S'
    elif item == Question:
        item = 'Q'
    try:
        return Template.objects.get(type=item).template
    except (Template.DoesNotExist, AttributeError):
        return ""


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
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


def cleanup_for_search(raw_text):
    """
    Cleanup raw_text to be suited for matching in search.
    Operations:
      - Strip HTML tags
      - Remove newlines, returns and tab characters
      - Trim double and trailing spaces
      - Convert to lower case
      - Remove URLs
      - Remove email addresses
    """
    # Strip HTML tags
    text = strip_tags(raw_text)
    # Remove newlines, returns and tab characters
    text = re.sub(r"[\t\n\r]", "", text)
    # Trim double and trailing spaces
    text = re.sub(r" +", " ", text).strip()
    # Convert to lower case
    text = text.lower()
    # Remove URLs
    text = re.sub(r'\b(https?|ftp)://[^\s/$.?#].[^\s]*\b', "", text)
    # Remove email addresses
    text = re.sub(r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}\b', "", text)
    return text


class Tag(models.Model):
    TAG_TYPES = (('P', 'Pedagogy'),
                 ('T', 'Technology'),
                 ('C', 'Content'),
                 ('O', 'Context/Topic'))
    # The type of this tag, used for coloring
    type = models.CharField(max_length=1, choices=TAG_TYPES)
    # The handle by which this tag will be identified
    handle = models.CharField(max_length=255, unique=True)
    # The glossary item that explains the tag
    glossary = models.ForeignKey('Glossary', on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    # The reference to the Tag of which this is an alias (if applicable)
    alias_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

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
                'info': info_dict,
                'get_absolute_url': self.get_absolute_url()}

    def __str__(self):
        s = dict(self.TAG_TYPES)[self.type] + ":" + self.handle
        if self.alias_of:
            s += ' > ' + self.alias_of.handle
        return s

    def get_absolute_url(self):
        return '/tag/' + str(self.handle)

    class Meta:
        ordering = ['type', 'handle']


class Template(models.Model):
    type = models.CharField(max_length=1, choices=ITEM_TYPES, primary_key=True)
    template = ck_field.RichTextUploadingField(verbose_name='Text')

    def __str__(self):
        return dict(ITEM_TYPES)[self.type] + " template"

    def __repr__(self):
        return dict(ITEM_TYPES)[self.type] + " template"


class Community(models.Model):
    # The name of the community
    name = models.CharField(max_length=254)
    #abbreviation = models.CharField(max_length=50, blank=True, null=True,
    #                                default=None)
    # Communities are hierarchical
    part_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                default=None, related_name="subcommunities")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Community(%s)" % (self.name,)

    def get_parents(self):
        if self.part_of is not None:
            return [self.part_of] + self.part_of.get_parents()
        return []


class Link(models.Model):
    from_item = models.ForeignKey('Item',on_delete=models.CASCADE, related_name='+')
    to_item = models.ForeignKey('Item',on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return "%s -> %s" % (str(self.from_item), str(self.to_item))

    def save(self, *args, **kwargs):
        reflexive = True if self.pk is None else False
        super(Link, self).save(*args, **kwargs)

        # Make link reflexive
        if reflexive:
            self.to_item.link(self.from_item)


class Item(models.Model):
    # Tags linked to this item
    tags = models.ManyToManyField('Tag', blank=True)
    # The other items that are linked to this item
    links = models.ManyToManyField('Item', blank=True, through='Link',
            symmetrical=False)
    # The comments linked to this item
    comments = models.ManyToManyField('Comment', blank=True, editable=True)
    # Whether this item is featured by a moderator
    featured = models.BooleanField(default=False)
    # The type of this item, important to know which subclass to load
    type = models.CharField(max_length=1, choices=ITEM_TYPES, editable=False)
    # The score of this item, which can be used for ranking of search results
    score = models.IntegerField(default=0)
    # The date that this item was created in the database
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    # The concatenated string representation of each item for free text search
    searchablecontent = models.TextField(editable=False)
    # The communities for which the item is visible
    communities = models.ManyToManyField('Community',
            related_name='items')

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

    def save(self, *args, **kwargs):
        # If new instance is created, set the default community (public)
        super(Item, self).save(*args, **kwargs)
        if self.pk is None:
            self.communities.add(Community.objects.get(pk = 1))

    @property
    def display_name(self):
        return self.__str__()

    def summary(self):
        return ""

    def link(self, link):
        Link.objects.get_or_create(from_item=self, to_item=link)

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
            'type': dict(ITEM_TYPES)[self.type],
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
        if self.type in dict(ITEM_TYPES):
            t = dict(ITEM_TYPES)[self.type].lower().replace(" ", "")
            return '/' + t + "/" + str(self.id)
        else:
            return '/item/' + str(self.id)

    def __str__(self):
        # Attempt to get reference to subclass
        subcls = self.downcast()
        if subcls is not None:
            return subcls.__str__()
        else:
            return self.searchablecontent[:40]

    def save_dupe(self):
        super(Item, self).save()


class Comment(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    text = ck_field.RichTextUploadingField()
    author = models.ForeignKey('Person', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    upvoters = models.ManyToManyField('Person', related_name='upvoters',
                                      blank=True)
    downvoters = models.ManyToManyField('Person', related_name='downvoters',
                                        blank=True)

    def __str__(self):
        return str(self.text[:40],)

    @property
    def votes(self):
        return self.upvoters.all().count() - self.downvoters.all().count()

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
    about = models.TextField(blank=True)
    # The source of a photo
    photo = models.URLField(blank=True)
    # The website of this person
    website = models.URLField(max_length=255, null=True, blank=True)
    # The email address of this person
    email = models.EmailField(null=True)
    # User corresponding to this person. If user deleted, person remains.
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
                                blank=True)
    # The ID given by some external auth-service
    external_id = models.CharField(max_length=255, null=True, blank=True)

    # Show the email addres on public pages
    public_email = models.BooleanField(default=True,
        verbose_name="Make email public")

    class Meta:
        ordering = ['name']

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.type = 'P'

    def summary(self):
        return self.headline

    @property
    def display_name(self):
        return self.name

    def display_handle(self):
        return u"@%s" % (self.handle,)
    display_handle.short_description = "Handle"

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

    def __str__(self):
        return "[Person] %s" % (self.name,)

    def save(self, *args, **kwargs):
        texts = [cleanup_for_search(self.name),
                 cleanup_for_search(self.about),
                 cleanup_for_search(self.headline)]
        self.searchablecontent = "<br />".join(texts)
        super(Person, self).save(*args, **kwargs)


class TextItem(Item):
    # The title of the good practice
    title = models.CharField(max_length=255)
    # The WYSIWYG text of the good practice
    text = ck_field.RichTextUploadingField(verbose_name='Text')
    # The person who created the good practice
    author = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, related_name='+')

    def display_author(self):
        if self.author is not None:
            return self.author.name
        else:
            return "<No author>"
    display_author.short_description = "Author"

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

    def __str__(self):
        return "[%s] %s" % (dict(ITEM_TYPES)[self.type], self.title)

    @property
    def display_name(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        self.searchablecontent = "<br />".join([cleanup_for_search(self.title),
                                                cleanup_for_search(self.text)])
        # On create, not update
        if self.pk is None:
            super(TextItem, self).save(*args, **kwargs)
            # Add self to author links
            if not self in self.author.links.all():
                self.author.link(self)
                self.author.save()

        # Link to the author
        self.link(self.author)

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
    contact = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='+')
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
    contact = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='+')
    # The date of the event
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, default='')

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

    def __str__(self):
        return "[Question] %s" % (self.title,)


class Glossary(TextItem):
    def __init__(self, *args, **kwargs):
        super(Glossary, self).__init__(*args, **kwargs)
        self.type = 'S'


# Queries can be stored to either be displayed on the main page, rss feed or to
# allow persons to subscribe to the query in order to be notified if the
# results are updated (i.e. new results can be found).
class SearchQuery(models.Model):
    # Which tags are mentioned in the query
    tags = models.ManyToManyField(Tag, related_name='in_queries')
    # Which persons are mentioned in the query
    persons = models.ManyToManyField(Person,
                                     related_name='in_queries')
    # What was the last known (cached) result of this query
    result = models.ManyToManyField(Item, related_name='result_of')
    # When was the query stored
    stored = models.DateTimeField(auto_now=True)


# Subscriptions indicate to update the reader if results of a query change
class Subscription(models.Model):
    # What query is subscribed to?
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, null=False)
    # Who is subscribing to this query (to contact this person later)
    reader = models.ForeignKey(Person, on_delete=models.CASCADE, null=False)


# DisplayQueries indicate to show the query on the homepage
class DisplayQuery(models.Model):
    # The query that is displayed
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, null=False)
    # The template to use when rendering
    template = models.CharField(max_length=100)
