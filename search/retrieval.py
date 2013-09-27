from django.db import models
from django.http import HttpResponse
from django.db.models import Q

from search.models import *
from search import utils

def retrieve(querystring):
    '''
    A query contains one or more of the following tokens
    @ - indicates user
    # - indicates tags
    " - indicates literal

    Any query is a conjunction of disjunctions of similar tags:
    (#tag1 v #tag2 v #tag3) ^ (@user1 v @user2) ^ "literal"
    '''
    tags, handles, literals = utils.parsequery(querystring)
    results = []

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

    # Create a filter for tags that includes alias_of
    relevant_persons = Person.objects.filter(
                           createfilter('handle', handles, False)
                       )
    relevant_tags = Tag.objects.filter(
                        createfilter('name', tags, False) |
                        createfilter('tags__alias_of', tags, False)
                    )
    relevant_items = Item.objects.select_related().filter(
                         createfilter('tags', list(relevant_tags), False) &
                         createfilter('searchablecontent__contains',
                                      literals, True) &
                         createfilter('links', list(relevant_persons), False)
                     )
    # Determine type and for each set, use individual query
    # TODO make of use automatic downcasting (or not)
    infos = list(relevant_items.filter(type='I'))
    questions = list(relevant_items.filter(type='Q'))

    # If queried, return these
    results = []
    for person in relevant_persons:
         results.append({
                            'type': 'Person',
                            'full_name': person.full_name,
                            'starred': person.starred,
                            'score': person.score,
                            'tags': get_tags(person)
                         })
    for info in (i.info for i in infos):
        results.append({
                            'type': 'Info',
                            'info_type': info.info_type,
                            'title': info.title,
                            'starred': info.starred,
                            'pub_date': info.pub_date,
                            'exp_date': info.exp_date,
                            'tags': get_tags(info)
                       })
    for question in (t.question for t in questions):
        results.append({
                            'type': 'Question',
                            'title': question.title,
                            'date': question.date,
                            'tags': get_tags(question)
                        })

    return querystring, results
