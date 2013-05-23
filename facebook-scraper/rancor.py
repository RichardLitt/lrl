'''
"My rancor seeks flesh!" - A Night Sister
(How the above quote is relevant I have yet to discover.)

Phonotactic inducer and language identifier

Richard Littauer
'''

# UPS them in, folks.
import sys
import random
import re
import operator

# Input and main output files
test = 'test_corpus'
output_file = 'output_file'
output = open(output_file, 'w+')

# How about we establish what files we're using as test examples?
swahili_input = 'genesis_swa'
rangi_input = 'genesis_lan'
english_input = 'genesis_eng'

# Let's open the files, ok?
swahili_in = open(swahili_input, 'r+')
rangi_in = open(rangi_input, 'r+')
english_in = open(english_input, 'r+')

# And maybe read the lines for each one.
swaList = swahili_in.read()
ranList = rangi_in.read()
engList = english_in.read()

def rangi_vowels(langList):
    # Letter set
    inventory = sorted(set(langList))
    special_vowels = ['\xc9','\xc3','\xca', '\xc6']
    letters = inventory[11:-18] + special_vowels
    delete = inventory[-18:]+inventory[3:11]

    for x in special_vowels:
        if x in delete: delete.remove(x)
 

    # Vowels and consonants
    vowels = ['a','e','i','o','u','A','E','I','O','U',\
            '\xc9','\xc3','\xca', '\xc6']
    consonants = []
    glides = ['w', 'y']
    for item in letters:
        if item not in vowels:
            if item not in glides:
                consonants.append(item)

    return vowels, consonants, glides, delete

def swahili_vowels(langList):
    # Letter set
    inventory = sorted(set(langList))
    letters = inventory[10:-7]
    delete = inventory[-7:]+inventory[3:10]

    # Vowels and consonants
    vowels = ['a','e','i','o','u','A','E','I','O','U']
    consonants = []
    glides = ['w', 'y']
    for item in letters:
        if item not in vowels:
            if item not in glides:
                consonants.append(item)

    return vowels, consonants, glides, delete

def english_vowels(langList):
    # Letter set
    inventory = sorted(set(langList))
    letters = inventory[19:-4]
    delete = inventory[-4:]+inventory[2:19]

    # Vowels and consonants
    vowels = ['a','e','i','o','u','A','E','I','O','U']
    consonants = []
    glides = ['w', 'y']
    for item in letters:
        if item not in vowels:
            if item not in glides:
                consonants.append(item)

    return vowels, consonants, glides, delete

def vowels_and_consonants(langList, output, language):

    if language == 'english':
        vowels, consonants, glides, delete = english_vowels(langList)
    if language == 'swahili':
        vowels, consonants, glides, delete = swahili_vowels(langList)
    if language == 'rangi':
        vowels, consonants, glides, delete = rangi_vowels(langList)


    # Word set
    for x in delete: 
        langList = langList.replace(x, '')
    langList = langList.replace('\n', '')
    langList = langList.replace('\t', '')
    wordlist = langList.split(' ')

    # Put in some beginning and end of word marks.
    for word in range(len(wordlist)):
        wordlist[word] = '<' + wordlist[word] + '>'

    # Anonymise each word until we're left with structures
    structures_uncounted = []
    for word in wordlist:
        structure = ''
        for letter in range(len(word)):
            if word[letter] in vowels:
                structure += 'V'
            if word[letter] in glides:
                structure += 'y'
            if word[letter] in consonants:
                structure += 'C'
        structures_uncounted.append(structure)

    # We're going to normalise this by dividing over the entire list.
    normalise = float(len(wordlist))

    # Count the structures
    structures_unsorted = {}
    for item in structures_uncounted:
        result = structures_uncounted.count(item)/normalise
        if item not in structures_unsorted:
            structures_unsorted[item] = result

    structures = sorted(structures_unsorted.iteritems(), key=operator.itemgetter(1),\
        reverse=True)

    print structures
    for x in range(len(structures)): 
        output.write(structures[x][0] + '\t' + str(structures[x][1])+'\n')

    output.close

def trigram(langList, output, language):

    if language == 'english':
        vowels, consonants, glides, delete = english_vowels(langList)
    if language == 'swahili':
        vowels, consonants, glides, delete = swahili_vowels(langList)
    if language == 'rangi':
        vowels, consonants, glides, delete = rangi_vowels(langList)


    # Word set
    for x in delete: 
        langList = langList.replace(x, '')
    langList = langList.replace('\n', '')
    langList = langList.replace('\t', '')
    wordlist = langList.split(' ')

    # Put in some beginning and end of word marks.
    for word in range(len(wordlist)):
        wordlist[word] = '<' + wordlist[word] + '>'

    # Guess we don't need to anonymise anymore
    valid_strings = {}
    # Or do things slowly
    fastwordlist = ''.join(wordlist)

    # So, what are the letters currently being used? 
    inventory = sorted(set(fastwordlist))

    # For each trigram, make an entry
    for letter in inventory:
        for letter_two in inventory:
            for letter_three in inventory:
                string = letter + letter_two + letter_three
                escape = 0

                # No need to have an unigram analysis.
                if (letter == ">") or (letter == "<"): escape += 1
                if (letter_three == ">") or (letter_three == "<"): escape += 1
                if (letter_two == ">") or (letter_two == "<"): escape += 1
                if escape <= 1:
                    count = fastwordlist.count(string)
                    if count != 0:
                        valid_strings[string] = count

    # Sort those.
    valid_strings = sorted(valid_strings.iteritems(), key=operator.itemgetter(1),\
        reverse=True)

    # Normalisation
    normalise = 0
    for x in range(len(valid_strings)): normalise += valid_strings[x][1]

    # And print it all out. 
    for x in range(len(valid_strings)): 
        output.write(valid_strings[x][0] + '\t' + \
                str(valid_strings[x][1]/float(normalise))+'\n')

    output.close()

'''
Testing
'''

test = open(test, 'r+')
lineList = test.readlines()

def test(output_file):
    output = open(output_file, 'w+')
    corpus = []
    for line in lineList:
        # This converts it to an easier format to deal with
        lang = re.compile('lang=".*" >')
        match_lang = re.search(lang, line)
        if match_lang != None:
            lang = match_lang.group(0).replace('lang="','').replace('" >','')
            lang = '  __' + lang[0] + '__  '
        pattern = re.compile(">.*")
        match_re = re.search(pattern, line)
        if (match_re != None):
            string = match_re.group(0).strip('</text>').replace('\n', ' ')
            corpus.append(lang + string + lang)
    corpus = ''.join(corpus)

    english = {}; swahili = {}; rangi = {}
    engvc = open('engvc', 'r+'); engvc = engvc.readlines()
    for line in engvc: 
        line = line.split('\t'); 
        english[line[0]] = line[1]
    swavc = open('swavc', 'r+'); swavc = swavc.readlines()
    for line in swavc: line = line.split('\t'); swahili[line[0]] = line[1]
    ranvc = open('ranvc', 'r+'); ranvc = ranvc.readlines()
    for line in ranvc: line = line.split('\t'); rangi[line[0]] = line[1]


    englisht = {}; swahilit = {}; rangit = {}
    engtri = open('engtri', 'r+'); engtri = engtri.readlines()
    for line in engtri: 
        line = line.split('\t'); 
        englisht[line[0]] = line[1]
    swatri = open('swatri', 'r+'); swatri = swatri.readlines()
    for line in swatri: line = line.split('\t'); swahilit[line[0]] = line[1]
    rantri = open('rantri', 'r+'); rantri = rantri.readlines()
    for line in rantri: line = line.split('\t'); rangit[line[0]] = line[1]


    # Let's start identifying
    language_now = 'e'
    accuracy = 0
    total = 0
    vowels, consonants, glides, delete = rangi_vowels(ranList)
    for x in range(len(corpus)):
        if corpus[x] == '_': continue
        if corpus[x] != '_':
            if corpus[x+1] == '_': continue
            if corpus[x+2] != '_': 
                if corpus[x+5] == '_':
                    if corpus[x+7] == '_':
                        language_now = corpus[x+6]
                
                # This is by VC()
                if sys.argv[2] == 'split':
                    phrases = corpus.split('    ')
                    for phrase in phrases:
                        phrase = phrase.split(' ')
                        for letter in range(len(phrase)):
                            word = ''
                            word_value = {}
                            for let in range(len(phrase[letter])):
                                if phrase[letter][let] in vowels:
                                    word += 'V'
                                if phrase[letter][let] in glides:
                                    word += 'y'
                                if phrase[letter][let] in consonants:
                                     word += 'C'
                            if word in english: 
                                word_value['e'] = english[word]
                            if word in swahili:
                                word_value['s'] = swahili[word]
                            if word in rangi:
                                word_value['r'] = rangi[word]
                            # Sort those.
                            try: best = sorted(word_value.iteritems(), \
                                    key=operator.itemgetter(1),\
                                reverse=True)[0][0]
                            except: best = ''
                            if best == language_now:
                                accuracy += 1
                                total += 1
                            if best != language_now:
                                accuracy += 0
                                total += 1
                    print accuracy / float(total)

                if sys.argv[2] == 'tri':
                    # Word set
                    for x in delete: 
                        corpus = corpus.replace(x, '')
                    corpus = corpus.split(' ')
                    # Put in some beginning and end of word marks.
                    for word in range(len(corpus)):
                        if corpus[word] != '':
                            if corpus[word][:2] != '__':
                                corpus[word] = '<' + corpus[word] + '>'
                    corpus = ''.join(corpus)
                    for y in range(len(corpus)):
                        word = corpus[y:y+3]
                        word_value = {}
                        if word in englisht: word_value['e'] = englisht[word]
                        if word in swahilit: word_value['s'] = swahilit[word]
                        if word in rangit: word_value['r'] = rangit[word]
                        # Sort those.
                        try: best = sorted(word_value.iteritems(), \
                                key=operator.itemgetter(1),\
                            reverse=True)[0][0]
                        except: best = ''
                        if best == language_now:
                            accuracy += 1
                            total += 1
                        if best != language_now:
                            accuracy += 0
                            total += 1
                        value = accuracy / float(total)
                        print y, value
                        output.write(str(y) + '\t' +  str(value) + '\n')


if __name__ == '__main__':
    if sys.argv[1] == 'train':
        if sys.argv[2] == "-vc":

            # Output files
            engvc = open('engvc', 'w+')
            swavc = open('swavc', 'w+')
            ranvc = open('ranvc', 'w+')

            vowels_and_consonants(engList, engvc, 'english')
            vowels_and_consonants(swaList, swavc, 'swahili')
            vowels_and_consonants(ranList, ranvc, 'rangi')

        if sys.argv[2] == "-3":

            # Output files
            engtri = open('engtri', 'w+')
            swatri = open('swatri', 'w+')
            rantri = open('rantri', 'w+')

            trigram(engList, engtri, 'english')
            trigram(swaList, swatri, 'swahili')
            trigram(ranList, rantri, 'rangi')

    if sys.argv[1] == 'test':
        test(output_file)
