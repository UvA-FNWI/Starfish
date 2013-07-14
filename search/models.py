from django.db import models


# pedagogy
class P(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


# technnics
class T(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


# category
class C(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    p = models.ManyToManyField(P, blank=True)
    t = models.ManyToManyField(T, blank=True)
    c = models.ManyToManyField(C, blank=True)

    full_name = models.CharField(max_length=70)
    starred = models.BooleanField(default=False)

    def __unicode__(self):
        return self.full_name


class Info(models.Model):
    INFO_TYPES = (('GP', 'Good Practice'),
                  ('IN', 'Information'),
                  ('MT', 'Meetings'))

    p = models.ManyToManyField(P, blank=True)
    t = models.ManyToManyField(T, blank=True)
    c = models.ManyToManyField(C, blank=True)

    title = models.CharField(max_length=70)
    text = models.TextField()
    authors = models.ManyToManyField(Person)

    date = models.DateTimeField(auto_now=True)
    starred = models.BooleanField(default=False)
    type = models.CharField(max_length=2, default='IN', choices=INFO_TYPES)

    def __unicode__(self):
        return self.title
