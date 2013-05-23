# This is a very simple counter to check how many characters and words there are
# in the file by simply joining together all of the <plaintext /> elements.

import re
from BeautifulSoup import BeautifulSoup

file = "output_pretty.xml"
f = open(file, 'r+')
f = f.readlines()
f = ''.join(map(str.strip,f))
f = BeautifulSoup(f)
f = f.findAll('plaintext')
g = []
for item in f:
    g.append(str(item))
f = ' '.join(g)
print len(f)
f = f.split(' ')
print len(f)
