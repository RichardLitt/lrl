import sys, re

file_open = sys.argv[1]
output_file_name = 'genesis_rangi'
output = open(output_file_name,'w+')

f = open(file_open, 'r+')
lineList = f.read()

characters = sorted(set(lineList))
print characters
for character in characters:
    try:
        character = character.decode('latin-1', 'replace')
    except:
        character = character.decode('ascii', 'replace')
    output.write(character)
