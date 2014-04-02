from django.dispatch import Signal, receiver
from django.core.mail import EmailMultiAlternatives
from search.models import Person
import logging

from starfish.settings import ADMIN_NOTIFICATION_EMAIL
unknown_tag_signal = Signal(providing_args=['author', 'title', 'tags'])
logger = logging.getLogger('search')


@receiver(unknown_tag_signal)
def unknown_tag_callback(sender, **kwargs):
    author = Person.objects.get(pk=kwargs['author'])
    title = kwargs['title']
    unknown_tags = kwargs['tags']
    message = "{person} created an item '{title}'".format(person=author.name,
                                                          title=title) + \
              "and tried to add the following nonexisting tags:\n" + \
              "Tokens: " + ','.join(unknown_tags['token']) + "\n" + \
              "Persons: " + ','.join(unknown_tags['person']) + "\n" + \
              "Literals: " + ','.join(unknown_tags['literal']) + "\n\n" + \
              "This message was generated automatically."
    logger.debug(message)
    subject = 'User {person} uses unknown tags'.format(person=author.name)
    from_email = "notifications@HOSTNAME"
    msg = EmailMultiAlternatives(subject, message, from_email,
                                 to=ADMIN_NOTIFICATION_EMAIL)
    msg.send(fail_silently=True)
