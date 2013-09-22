def parsequery(inputstring):
    # Tokenize, get tags/users/queries
    tags = set([])
    persons = set([])
    literals = set([])

    word = ''
    i = 0

    print inputstring

    inputstring+='+'
    while i < len(inputstring[:-1]):
        token = inputstring[i]
        next_token = inputstring[i+1]
        if token == "\\" or token == "+":
            pass
        elif token == "'":
            word = ''
            i += 1
            while i != len(inputstring):
                if inputstring[i] == "'":   # if legal end of literal, add it
                    literals.add(word.replace('+', ' ').strip())
                    break
                word += inputstring[i]
                i += 1
            word = ''
        elif next_token == '+':                  # end of word
            if word[0] == '#':              # word is Tag (name)
                tags.add(word[1:] + token)
                word = ''
            elif word[0] == '@':            # word is Person (handle)
                persons.add(word[1:] + token)
                word = ''
        else:
            word += token
        i += 1
    return list(tags), list(persons), list(literals)


if __name__=='__main__':
    print parsequery("@auke+#sometag+'@abc+#def+ghi'")
