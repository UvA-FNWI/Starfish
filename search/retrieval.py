from django.db import models

from steep.settings import SEARCH_SETTINGS
from search.models import Item, Tag, Person
from search import utils


def retrieve(query, dict_format = False):
    '''
    A query contains one or more tokens starting with the following symbols
    @ - indicates user
    # - indicates tags
    " - indicates literal

    These special specials are specified in the SEARCH_SETTINGS setting

    Any query is a conjunction of disjunctions of similar tokens:
    (#tag1 v #tag2 v #tag3) ^ (@user1 v @user2) ^ "literal"
    '''

    # Parse query into tag, person and literal tokens
    tag_tokens, person_tokens, literal_tokens = utils.parse_query(query)

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
        tags = Tag.objects.select_related('alias_of').filter(
            handle__in = tag_tokens)

        # Add tag aliases
        tags_extended = set([])
        for tag in tags:
            tags_extended.add(tag)
            if tag.alias_of is not None:
                tags_extended.add(tag.alias_of)
            else:
                # If this tag is not an alias,
                # check if other tags are an alias of this tag.
                for alias in Tag.objects.filter(alias_of=tag):
                    tags_extended.add(alias)
        # Use the extended set as list of tags
        tags = list(tags_extended)
    else:
        # Else, set tags to be empty
        tags = []

    # If persons were used
    if len(person_tokens) > 0:
        # If settings set to allow partial person handles
        if SEARCH_SETTINGS['allowPartialPersonHandles']:
            persons = Person.objects.filter(
                handle__iregex=r'^(' + '|'.join(person_tokens) + ')')
        else:
            persons = Person.objects.filter(
                handle__iregex=r'^(' + '|'.join(person_tokens) + ')$')
    else:
        # Else, set persons to be empty
        persons = []

    # If no useful elements could be found in the query
    if len(persons)+len(literals)+len(tags) == 0:
        # Return an empty result
        return query, []

    items = Item.objects.select_related()
    # Add literal contraints
    if len(literals) > 0:
        # For each literal add a constraint
        for literal in literals:
            items = items.filter(searchablecontent__contains = literal)

    # Add tag constraints
    tags_by_type = {}
    for tag in tags:
        key = tag.type
        if key in tags_by_type:
            tags_by_type[key].append(tag)
        else:
            tags_by_type[key] = [tag]

    if len(tags) > 0:
        for tags in tags_by_type.values():
            items = items.filter(tags__in = tags)

    # Add person constraints
    if len(persons) > 0:
        items = items.filter(links__in = persons)

    # Retrieve the elements
    items = list(items)

    # If settings set to always include mentioned persons
    if SEARCH_SETTINGS['alwaysIncludeMentionedPersons']:
        # If persons were used in filter
        if len(persons) > 0:
            # Add them to the items as well
            for person in persons:
                items.append(person)

    # Ensure items to contain no duplicates
    items = list(set(items))

    # Initialize results
    results = []

    # Generate search results
    if dict_format:
        for item in items:
            # Append the dict_format representation of the item to the results
            results.append(item.dict_format())
    else:
        results = items

    # Return the original query and the results
    return query, results
