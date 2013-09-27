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

def ensure_info(info_type, title, text):
    info, created = Info.objects.get_or_create(
            info_type=info_type, title=title, text=text)
    if created:
        info.save()
    return info

def populate():
    # Tags
    t1 = ensure_tag('O', "LearningAnalytics")
    t2 = ensure_tag('O','Toetsen en toetsgestuurd leren')
    t3 = ensure_tag('O', "Afstand onderwijs en zelfstandig leren")
    t4 = ensure_tag('O', "Nieuwe Onderwijsconcepten")
    t5 = ensure_tag('T', "Blackboard")
    t6 = ensure_tag('T', "Stemkasjes")

    # People
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

    NatasaBrouwer.tags.add(t1)
    AndreHeck.tags.add(t1)
    NatasaBrouwer.tags.add(t2)
    NatasaBrouwer.tags.add(t3)
    NatasaBrouwer.tags.add(t4)
    NatasaBrouwer.tags.add(t5)
    NatasaBrouwer.tags.add(t6)
    ErwinVanVliet.tags.add(t6)

    # Info
    peerinstruction = ensure_info(
        'IN',
        "Peer-instruction",
        "Peer-instruction is een onderwijsmethode om studenten te activeren"
        " voor leren. Met deze methode kunnen misconcepties worden opgespoord"
        " en verholpen."
        " Deze methode is ontwikkeld door Eric Mazur (Natuurkunde, Harvard"
        " University). Deze is gebaseerd op de techniek \"Think-Pair-Share\","
        " een collaborative onderwijs techniek uit jaren 80."
        " De essentie van peer-instruction methode is dat eerst een vraag aan"
        " studenten wordt gesteld om individueel over na te denken,"
        " vervolgens geven ze door het stemmen een antwoord op de vraag. Bij"
        " een verdeling van antwoorden wordt studenten gevraagd om met de"
        " buurman die een andere antwoord heeft gegeven de vraag te"
        " bespreken. Vervolgens wordt het opnieuw gestemd over de vraag. De"
        " docent vat samen en geeft nog uitleg indien nodig. In een college"
        " kan de peer-instruction cyclus bij meerdere onderwerpen gebruikt"
        " worden.<br /><br />"
        " Schema (plaatje) - Scenario van peer-instruction<br /><br />"
        " Deze methode wordt vaak gecombineerd met flipped classroom."
        " Eric Mazur heeft onderzoek gedaan naar effecten van"
        " peer-instruction.<br /><br />"
        "Literatuur en verwijzingen (body):"
        "<ul>"
        "<li>"
        "Mazur, M. (2009) Farewell, Lecture?, Science, 232, pp. 50-51."
        "<li>"
        "Crouch, C.H., Mazur, M. (2011), Peer Instruction: Ten years of"
        " experience and results, Am. J. Phys. 69 (9), 970-977."
        "</li>"
        "<li>"
        "Turn to your neighbour, de peer-instruction blog"
        " http://blog.peerinstruction.net"
        "</li>"
        "<li>"
        "Video's Eric Mazur: From Questions to concepts"
        " http://www.youtube.com/watch?v=lBYrKPoVFwg"
        "</li>"
        "<li>"
        "Eric Mazur: Confessions of converted lecturer (talk):"
        " http://www.youtube.com/watch?v=WwslBPj8GgI"
        "</li>"
        "<li>"
        "Quote Eric Mazur: \"I thought I was a good teacher until I"
        " discovered my students were just memorizing information rather than"
        " learning to understand the material. Who was to blame? The"
        " students? The material? I will explain how I came to the agonizing"
        " conclusion that the culprit was neither of these. It was my"
        " teaching that caused students to fail! I will show how I have"
        " adjusted my approach to teaching and how it has improved my"
        " students' performance significantly.\"" 
        "</li><br /><br />"
        "Eric Mazur<br />"
        "Professor of Physics and Applied Physics at Harvard University."
        " Leads a vigorous research program in optical physics and supervises"
        " one of the largest research groups in the Physics Department at"
        " Harvard University."
    )
    peerinstruction.tags.add(t2)
    peerinstruction.tags.add(t3)
    peerinstruction.links.add(NatasaBrouwer)
    peerinstruction.links.add(ErwinVanVliet)
