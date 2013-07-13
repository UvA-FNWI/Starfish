from django.db import models


# pedagogy
class P(models.Model):
    name = models.CharField(max_length=255, unique=True)


# technnics
class T(models.Model):
    name = models.CharField(max_length=255, unique=True)


# category
class C(models.Model):
    name = models.CharField(max_length=255, unique=True)


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

    type = models.CharField(max_length=2, choices=INFO_TYPES)
    text = models.TextField()
    date = models.DateField()
    starred = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text
