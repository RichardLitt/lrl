'''
This creates a mixed test corpus from three corpora.
Richard Littauer
'''

# Let's UPS some things in.
import sys, random

# How about we establish what files we're using as test examples?
swahili_input = 'genesis_swa'
rangi_input = 'genesis_lan'
english_input = 'genesis_eng'

# Should we maybe store the file somewhere?
output_file = 'test_corpus'

# Or maybe we should open it too.
output = open(output_file, 'w+')

# Let's open the files, ok?
swa = open(swahili_input, 'r+')
ran = open(rangi_input, 'r+')
eng = open(english_input, 'r+')

# And maybe read the lines for each one.
swaList = swa.readlines()
ranList = ran.readlines()
engList = eng.readlines()

# Let's make it easy to randomly choose
total_corpus_selection = [swaList, ranList, engList]

# And to recall the names of what was chosen later.
named = ['swa', 'lan', 'eng']

# Let's make it 1000 samples long. That should be long enough, I think. 
for x in range(1000):
    
    # Choose a corpus.
    choice = random.randrange(len(total_corpus_selection))
    corpus_choice = total_corpus_selection[choice]

    # And then choose a line.
    selection = corpus_choice[random.randrange(len(corpus_choice))]\
            .replace('\n','')

    # And then split that line.
    selection = selection.split(' ')

    if len(selection) <= 1:
        string = ' '.join(selection)

    if len(selection) > 1:

        # From the beginning, choose a place to start.
        start = random.randrange(len(selection))
        
        # And from there, randomly choose a length to go with.
        # Yes, this does bias towards shorter strings.
        end = random.randrange(len(selection)-start)
        
        # The final selection
        string = selection[start:start+end]
        string = ' '.join(string)

    # No zeros please.
    if len(string) == 0:
            string = ' '.join(selection)

    string = '<text lang=\"' + named[choice] + '\" >'+string+'</text>\n'

    output.write(string)
