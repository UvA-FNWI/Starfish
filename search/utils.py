from django.http import HttpResponse

def parsequery(inputstring):
    # Tokenize, get tags/users/queries
    tags = set([])
    persons = set([])
    literals = set([])

    word = ''
    for token in inputstring:
        if token == '+':
            if word[0] == '#':    # Tag
                tags.add(word[1:])
                word = ''
            elif word[0] == '@':  # User
                persons.add(word[1:])
                word = ''
        elif len(word) and (word[0] == token == "'" or word[0] == token == "\""):
            literals.add(word[1:])
            word = ''
        else:
            word += token

    return tags, persons, literals
