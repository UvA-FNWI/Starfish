from django.db import models
from django.http import HttpResponse
from django.db.models import Q

from search.models import *
from search import utils

def retrieve(querystring):
    '''
    A query contains one or more tokens starting with the following symbols
    @ - indicates user
    # - indicates tags
    " - indicates literal

    These special specials are specified in the SEARCH_SYNTAX setting

    Any query is a conjunction of disjunctions of similar tags:
    (#tag1 v #tag2 v #tag3) ^ (@user1 v @user2) ^ "literal"
    '''

    def get_tags(item):
        return [{'name': t.name, 'type': t.type} for t in list(item.tags.all())]

    def createfilter(kw, lst, conjunct):
        '''
        Creates a disjunction of Qfilters based on keyword kw and a list
        of values for that keyword lst.
        '''
        if not lst:
            return Q()

        if conjunct:
            if len(lst) == 1:
                print kw
                return Q(**{kw: lst[0]})
            else:
                first_arg = lst.pop()
                return Q(**{kw: first_arg}) & createfilter(kw, lst, conjunct)
        else:
            if len(lst) == 1:
                return Q(**{kw: lst[0]})
            else:
                first_arg = lst.pop()
                return Q(**{kw: first_arg}) | createfilter(kw, lst, conjunct)


    # Parse query into tag, person and literal tokens
    tag_tokens, person_tokens, literal_tokens = utils.parse_query(querystring)

    # If literals were used
    if len(literal_tokens) > 0:
        # Store literals in a set
        literals = set([])
        # Lower all literals, and add them to the set
        for literal in literal_tokens:
            literals.add(literal.lower())
        # Convert the set back to a list
        literals = list(literals)
    else:
        # Else, set literals to be empty
        literals = []

    # If tags were used
    if len(tag_tokens) > 0:
        # Fetch all mentioned tags and their aliases
        tags = Tag.objects.select_related('alias_of').filter(name__in =
                tag_tokens)

        # Add tag aliases
        tags_extended = set([])
        for tag in tags:
            tags_extended.add(tag)
            if tag.alias_of is not None:
                tags_extended.add(tag.alias_of)
        # Use the extended set as list of tags
        tags = list(tags_extended)
    else:
        # Else, set tags to be empty
        tags = []

    # If persons were used
    if len(person_tokens) > 0:
        persons = Person.objects.filter(handle__in = person_tokens)
    else:
        # Else, set persons to be empty
        persons = []

    # If no useful elements could be found in the query
    if len(persons)+len(literals)+len(tags) == 0:
        # Return an empty result
        return querystring, []
    else:
        print "Search with:",persons, literals, tags

    items = Item.objects
    # Construct query items
    if len(literals) > 0:
        items = items.filter(
            createfilter('searchablecontent__contains',literals, True)
        )
        print items

    if len(tags) > 0:
        items = items.filter(tags__in = tags)
        print items

    if len(persons) > 0:
        items = items.filter(links__in = persons)
        print items

    # Retrieve the elements
    items = list(items)

    # If persons were used in filter
    if len(persons) > 0:
        # Add them to the items as well
        for person in persons:
            items.append(person)

    # Ensure items to contain no duplicates
    items = list(set(items))

    # Initialize results
    results = []

    # For all items
    for item in items:
        # Append the search_format representation of the item to the results
        results.append(item.search_format())

    # Return the original query and the results
    return querystring, results
