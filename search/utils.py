from steep.settings import SEARCH_SETTINGS
from search.models import Tag, Person

def parse_query(query):
    """
        Tokenize query into person, tag and literal tokens.
        Uses the special symbols as defined in the syntax setting.
    """
    # Get syntax
    syntax = SEARCH_SETTINGS['syntax']
    # Tokenize, get tags/users/queries
    tags = []
    persons = []
    literals = []

    # Initialize empty token
    token = None

    # Initialize symbol position
    i = 0
    # Initialize start position of token span
    a = 0

    # While query still contains symbols
    while i < len(query):
        # Eat symbol
        symbol = query[i]
        # If no token is being formed
        if token is None:
            # If symbol is the delimeter
            if symbol == syntax['DELIM']:
                # This means nothing in this context, but we do need to update
                # the span to prevent it from including this character
                a += 1
            # If symbol is the escape character
            elif symbol == syntax['ESCAPE']:
                # If a special character is being escaped
                if i < len(query)-1 and query[i+1] in syntax.values():
                    # Add the escape character + the escaped character
                    #  as normal symbols. The escape character will be taken
                    #  out later.
                    token = query[i]+query[i+1]
                    # Jump over the escaped character
                    i += 1
                    # Update span to prevent it from including this character
                    a += 1
                else:
                    # Ignore, means nothing in this context
                    pass
            # If symbol is literal character
            elif symbol == syntax['LITERAL']:
                # Start empty literal token
                token = ""
                # Jump to next character
                i += 1
                # Eat symbols until literal character or end of string
                while i < len(query):
                    # Eat symbol (inner loop)
                    symbol = query[i]
                    # If symbol is literal character
                    if symbol == syntax['LITERAL']:
                        # Add token to literals
                        literals.append((token,(a, a + len(token)+2)))
                        # Update start position of token span
                        a = i + 1
                        # Clear token
                        token = None
                        # Stop eating symbols for literal
                        break
                    # If symbol is the escape character
                    elif symbol == syntax['ESCAPE']:
                        # If the literal character is being escaped
                        if i < len(query)-1 and \
                                query[i+1] == syntax['LITERAL']:
                            # Add literal character as normal symbol
                            token += syntax['LITERAL']
                            # Jump over literal character
                            i += 1
                        # If a different symbol follows the escape character
                        else:
                            # Add escape character to token
                            token += syntax['ESCAPE']
                    else:
                        # Add symbol to literal token
                        token += symbol
                    i += 1
                # If literal token was not ended
                if token is not None:
                    # Add token to literals
                    literals.append((token, (a, a + len(token)+1)))
                    # Clear token
                    token = None
            # If symbol is something else
            else:
                # Start a new token with the symbol
                token = symbol
        # If a token is already being formed
        else:
            # If symbol is the delimeter
            if symbol == syntax['DELIM']:
                # If the token is a person
                if token[0] == syntax['PERSON']:
                    # Add the token (without syntax symbol) to persons
                    persons.append((token[1:],(a, a + len(token))))
                    # Update start position of token span
                    a = i + 1
                # If the token is a tag
                elif token[0] == syntax['TAG']:
                    # Add the token (without syntax symbol) to tags
                    tags.append((token[1:], (a, a + len(token))))
                    # Update start position of token span
                    a = i + 1
                # If the token is escaped
                elif token[0] == syntax['ESCAPE']:
                    # Treat the rest the token as literal
                    literals.append((token[1:], (a, a + len(token) - 1)))
                    # Update start position of token span
                    a = i + 1
                # If the token is a literal
                else:
                    # Add the token to the literals
                    literals.append((token, (a, a + len(token))))
                    # Update start position of token span
                    a = i + 1

                # Clear token
                token = None
            # If symbol is the escape character
            elif symbol == syntax['ESCAPE']:
                # If a special character is being escaped
                if i < len(query)-1 and query[i+1] in syntax.values():
                    # Add the character as normal symbol
                    token = query[i+1]
                    # Jump over the escaped character
                    i += 1
                else:
                    # Ignore, means nothing in this context
                    pass
            # If symbol is something else
            else:
                # Add symbol to token
                token += symbol
        # Jump to next symbol
        i += 1

    # If last token was not ended
    if token is not None:
        # If the token is a person
        if token[0] == syntax['PERSON']:
            # Add the token (without syntax symbol) to persons
            persons.append((token[1:], (a, a + len(token))))
        # If the token is a tag
        elif token[0] == syntax['TAG']:
            # Add the token (without syntax symbol) to tags
            tags.append((token[1:], (a, a + len(token))))
        # If the token is escaped
        elif token[0] == syntax['ESCAPE']:
            # Treat the rest the token as literal
            literals.append((token[1:], (a, a + len(token) - 1)))
        # If the token is a literal
        else:
            # Add the token to the literals
            literals.append((token, (a, a + len(token))))
        # Clear token
        token = None

    # Discard any empty tokens
    clean_fn = lambda x: filter(lambda c: c[0] != '', x)
    tags = clean_fn(tags)
    persons = clean_fn(persons)
    literals = clean_fn(literals)

    # Return found tags, persons and literals
    return list(tags), list(persons), list(literals)

def did_you_mean(tags, persons, literals, query, template="%s"):
    '''
    Discover literals that closely resemble tags or persons. Returns a
    suggested query with proposed improvements if any, otherwise it returns the
    same query.

    Example:
    ========
    The query:
      "literal TagName #Tag literal"
    will be returned as:
      "literal #TagName #Tag literal"

    Algorithm:
    ==========
    The algorithm tries to find a sequence of literals that can be matched,
    case insensitive, to a tag or person. The algorithm is greedy in that it
    tries to find as big of a chunk as possible to match. It does so by keeping
    two position indexes a and b that point to the start and end of the chunk
    respectively. This traversing is described in the following pseudo-code.

    Pseudo-code:
    ------------
    given array literals
    given function tag_or_person # checks if sequence can be matched
    given function add_to_suggestions # updates suggested query
    1. n = length(literals)
    2. a = 0
    3. b = n
    4. while a < n:
    5.    while b > a:
    6.        if not tag_or_person(literals[a:b]):
    7.            b = b - 1
    8.        else:
    9.            add_to_suggestions(a,b)
    A.            a = b
    B.            b = n
    C.    a = a + 1
    D.    b = n
    '''

    # Placeholder for did_you_mean suggestions for tags and persons
    #  Type is a dictionary mapping (literal => tag)
    dym = {}

    # The query that will be returned as a did you mean suggestion
    dym_query = query

    # The raw query that will be returned as a did you mean suggestion
    # This can be used to generate a link in order to execute the query 
    dym_query_raw = query

    # Declare function to extract a part of the token information
    extract_fn = lambda i: lambda x: x[i]

    # Get person symbol from search syntax
    s_person = SEARCH_SETTINGS['syntax']['PERSON']

    # Get tag symbol from search syntax
    s_tag = SEARCH_SETTINGS['syntax']['TAG']

    # 1. Init the length
    n = len(literals)
    # 2. Init the start index
    a = 0
    # 3. Init the end index
    b = n

    # 4. While the start index did not reach the end of the array
    while a < n:
        # 5. While the end index did not reach the start index
        while b > a:
            # Construct token out of literal span
            token = "".join(map(extract_fn(0), literals[a:b]))
            # Attempt to match a tag
            try:
                tag = Tag.objects.get(handle__iexact=token)
            # 6.1. If a tag cannot be matched
            except Tag.DoesNotExist:
                # Attempt to match a person
                try:
                    person = Person.objects.get(handle__iexact=token)
                # 6.2. If a person cannot be matched
                except Person.DoesNotExist:
                    # 7. Move the end index back one slot
                    b -= 1
                # 8. If a person could be matched
                else:
                    # If the person was not already mentioned somewhere else
                    if person.handle not in map(extract_fn(0), persons):
                        # 9. Add to suggestions
                        dym[(a,b)] = person
                    else:
                        dym[(a,b)] = None
                    # A. Set start index to end index
                    a = b
                    # B. Set end index to end of array
                    b = n
            # 8. If a person could be matched
            else:
                # If the tag was not already mentioned somewhere else
                if tag.handle not in map(extract_fn(0), tags):
                    # 9. Add to suggestions
                    dym[(a,b)] = tag
                else:
                    dym[(a,b)] = None
                # A. Set start index to end index
                a = b
                # B. Set end index to end of array
                b = n
        # C. Move the start index forward one slot
        a += 1
        # D. Move the end index to the end of the array
        b = n
    # Offsets in span positions due to the differences in characters between the
    # original text and the suggested one, init at 0
    offset = 0
    offset_raw = 0
    # Generate queries
    for span in dym:
        indexes = map(extract_fn(1), literals[span[0]:span[1]])
        # Caculate the actual span in the text string
        tspan = reduce(lambda x, y: (x[0], y[1]), sorted(indexes))
        # Construct handle text
        if dym[span] is None:
           handle = ""
        elif isinstance(dym[span], Person):
           handle = s_person+dym[span].handle
        else:
           handle = s_tag+dym[span].handle
        # Construct new dym_query with suggestion in place
        dym_query = "%s%s%s" % (
                dym_query[:tspan[0]+offset],
                template % (handle, ),
                dym_query[tspan[1]+offset:])
        # Update offset in dym_query coordinates
        offset += len(template % (handle,)) - len(query[tspan[0]:tspan[1]])
        # Construct new dym_query_raw with suggestion in place
        dym_query_raw = "%s%s%s" % (
                dym_query_raw[:tspan[0]+offset_raw],
                handle,
                dym_query_raw[tspan[1]+offset_raw:])
        # Update offset in dym_query_raw coordinates
        offset_raw += len(handle) - len(query[tspan[0]:tspan[1]])
    return dym_query, dym_query_raw
