#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
#########################
# This uses an online dictionary of Maltese - English and makes a little
# terminal-side random flashcard and lookup tool. As the dictionary is
# copyrighted, one can either download it locally or just use the script here
# as is to access the website if you have internet. The script will check if
# you have internet or not.
#
# No copyright. Released into the wild by Richard Littauer.
#########################

# Import some modules!
import sys
import random
import re
import urllib2

# Test if the internet is on or not using Google.
# From: http://stackoverflow.com/questions/3764291/checking-network-connection
def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.113.99',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

# Just sorts the dictionary roughly, cleaning out the extra html.
def sort():
    dict = []
    for line in file:
        line = line.strip().split('   ')
        if len(line) == 3:
            dict.append(line)
    return dict

# For flashcards of random words
def printout(language,amount):
    dict = sort()
    if language == 'list':
        print 'English\t\tMaltese\t\tPhonetics'
        for x in range(amount):
            entry = '\t'.join(dict[random.randrange(len(dict))])
            print '', entry

# For searching for specific english or maltese words.
def search(language, word):
    dict = sort()
    find = False
    for line in dict:
            if language in ('m', 'ma'): search_line = line[1]
            if language in ('e', 'ea'): search_line = line[0]
            pattern = re.compile(word, re.IGNORECASE)
            if language in ('m', 'e'):
                for x in range(len(search_line.split())):
                    match_o = re.match(pattern, search_line.split()[x])
                    if (match_o != None):
                        print '','\t'.join(line)
                        find = True
            if language in ('ma', 'ea'):
                for x in range(len(search_line.split())):
                    match_o = re.search(pattern, search_line.split()[x])
                    if (match_o != None):
                        print '','\t'.join(line)
                        find = True
    if find == False:
        print " I couldn't find this word. Ma stajtx insib din il-kelma."

if __name__ == "__main__":
    try:
        local = False
        if internet_on() == True:
            # These grab the html from the website directly, if you don't want to
            # store the dictionary locally.
            u = urllib2.urlopen('http://aboutmalta.com/language/engmal.htm') 
            file = map(str,u.readlines()) #Gets the html for real
            status = 'on'
        if internet_on() == False:
            # This uses a local file, which should be renamed to whatever you
            # download it as.
            try:
                file = open('English-Maltese Dictionary.html', 'r+')
                local = True
            except: 
                print ' I couldn\'t find the dictionary. \
                Ma stajtx insib din id-dizzjunarju.'
            status = 'off'

        language = sys.argv[1]

        # The three options: flashcard lists, or search
        if language in ('l', '-l', 'list', '-list'):
            amount = int(sys.argv[2])
            printout('list',amount)

        # Search with a maltese word
        if language in ('m', '-m', 'maltese', 'mal', '-maltese'):
            search('m',sys.argv[2])

        # Search with an english word
        if language in ('e', '-e', 'english', 'eng', '-english'):
            search('e',sys.argv[2])
        
        # Search with a maltese word
        if language == '-ma':
            search('ma',sys.argv[2])

        # Search with an english word
        if language == '-ea':
            search('ea',sys.argv[2])

        # The help desk!
        if language in ('h', 'help', '-h','--help', '--h'):
            print
            print 'Maltese-English Dictionary'
            print 'Richard Littauer. WTFPL License.'
            print 'https://github.com/RichardLitt/lrl'
            print
            print '\tPossible options:'
            print '\t\t-m [maltese word to translate]'
            print '\t\t-e [english word to translate]'
            print '\t\t-l [amount of words to list]'
            print '\tValid: m, -m, mal, maltese, -maltese'
            print 
            print '\t\t-ma [blind search for maltese string]'
            print '\t\t-ea [blind search for english string]'
            print
            print '\tInternet: %s.' % status
            if local: print '\tUsing local dictionary file.'
            else: pass
            print

    except IndexError:
        print ' This didn\'t work. Ma riditx tmur.'
        print ' Consult -help.'
