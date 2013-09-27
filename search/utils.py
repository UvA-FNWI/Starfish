from steep.settings import SEARCH_SYNTAX

def parse_query(query):
    """
        Tokenize query into person, tag and literal tokens.
        Uses the special symbols as defined in the SEARCH_SYNTAX setting.
    """
    # Tokenize, get tags/users/queries
    tags = set([])
    persons = set([])
    literals = set([])

    # Initialize empty token
    token = None

    # Initialize symbol position
    i = 0

    # While query still contains symbols
    while i < len(query):
        # Eat symbol
        symbol = query[i]
        # If no token is being formed
        if token is None:
            # If symbol is the delimeter
            if symbol == SEARCH_SYNTAX['DELIM']:
                # Ignore, means nothing in this context
                pass
            # If symbol is the escape character
            elif symbol == "\\":
                # If the literal character is being escaped
                if i < len(query)-1 and query[i+1] == SEARCH_SYNTAX['LITERAL']:
                    # Jump over literal character
                    i += 1
                else:
                    # Ignore, means nothing in this context
                    pass
            # If symbol is literal character
            elif symbol == SEARCH_SYNTAX['LITERAL']:
                # Start empty literal token
                token = ""
                # Jump to next character
                i += 1
                # Eat symbols until literal character or end of string
                while i < len(query):
                    # Eat symbol (inner loop)
                    symbol = query[i]
                    # If symbol is literal character
                    if symbol == SEARCH_SYNTAX['LITERAL']:
                        # Add token to literals
                        literals.add(token)
                        # Clear token
                        token = None
                        # Stop eating symbols for literal
                        break
                    # If symbol is the escape character
                    elif symbol == "\\":
                        # If the literal character is being escaped
                        if i < len(query)-1 and \
                                query[i+1] == SEARCH_SYNTAX['LITERAL']:
                            # Add literal character as normal symbol
                            token += SEARCH_SYNTAX['LITERAL']
                            # Jump over literal character
                            i += 1
                        # If a different symbol follows the escape character
                        else:
                            # Add escape character to token
                            token += "\\"
                    else:
                        # Add symbol to literal token
                        token += symbol
                    i += 1
                # If literal token was not ended
                if token is not None:
                    # Add token to literals
                    literals.add(token)
                    # Clear token
                    token = None
            # If symbol is something else
            else:
                # Start a new token with the symbol
                token = symbol
        # If a token is already being formed
        else:
            # If symbol is the delimeter
            if symbol == SEARCH_SYNTAX['DELIM']:
                # If the token is a person
                if token[0] == SEARCH_SYNTAX['PERSON']:
                    # Add the token (without syntax symbol) to persons
                    persons.add(token[1:])
                # If the token is a tag
                elif token[0] == SEARCH_SYNTAX['TAG']:
                    # Add the token (without syntax symbol) to tags
                    tags.add(token[1:])
                # If the token is a literal (one word)
                else:
                    # Add the token to the literals
                    literals.add(token)
                # Clear token
                token = None
            # If symbol is the escape character
            elif symbol == "\\":
                # If the literal character is being escaped
                if i < len(query)-1 and query[i+1] == SEARCH_SYNTAX['LITERAL']:
                    # Add literal character as normal symbol
                    token += SEARCH_SYNTAX['LITERAL']
                    # Jump over literal character
                    i += 1
                else:
                    # Ignore, means nothing in this context
                    pass
            # If symbol is literal character
            elif symbol == SEARCH_SYNTAX['LITERAL']:
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
        if token[0] == SEARCH_SYNTAX['PERSON']:
            # Add the token (without syntax symbol) to persons
            persons.add(token[1:])
        # If the token is a tag
        elif token[0] == SEARCH_SYNTAX['TAG']:
            # Add the token (without syntax symbol) to tags
            tags.add(token[1:])
        # If the token is a literal (one word)
        else:
            # Add the token to the literals
            literals.add(token)
        # Clear token
        token = None

    # Return found tags, persons and literals
    return list(tags), list(persons), list(literals)
