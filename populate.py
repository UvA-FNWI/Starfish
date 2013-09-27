from search.models import *

def name2handle(name):
    return "@"+"".join([ s.capitalize() for s in name.split(" ")])

def ensure_person(title, name, link, email):
    handle = name2handle(name)
    person, created = Person.objects.get_or_create(
            full_name = "%s %s" % (title, name),
            handle = handle,
            link = link,
            email = email)
    if created:
        person.save()
    return person

def ensure_tag(tag_type, title, alias=None):
    tag, created = Tag.objects.get_or_create(
            type=tag_type, name=title, alias_of=alias)
    if created:
        tag.save()
    return tag

def populate_persons():
    linkbase = "http://www.uva.nl/contact/medewerkers/item/"
    NatasaBrouwer = ensure_person(
        "Dr.",
        "Natasa Brouwer",
        linkbase+"n.brouwer-zupancic.html?f=Brouwer",
        "N.Brouwer-Zupancic@uva.nl")
    AndreHeck = ensure_person(
        "Dr.",
        "Andre Heck",
        linkbase+"a.j.p.heck.html?f=Heck",
        "A.J.P.Heck@uva.nl")
    ErwinVanVliet = ensure_person(
        "Dr.",
        "Erwin van Vliet",
        linkbase+"e.a.van-vliet.html?f=Vliet",
        "E.A.vanVliet@uva.nl")

    LearningAnalytics = ensure_tag('O', "LearningAnalytics")
    NatasaBrouwer.tags.add(LearningAnalytics)

