#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys #Arguments
import xlrd #Importing from excel
import codecs #Unicode support ##Might not be used - pylint this first.

output_file = "output.csv"

def grab(): 
	book = xlrd.open_workbook('roots.xls') # Open Spangola's list
	sheet = book.sheet_by_index(0) # Get the first sheet
	verbs = {}
	lastRowValues = {}
	for counter in range(sheet.nrows): # Loop for all possible rows
		# grab the current row
		rowValues = sheet.row_values(counter, start_colx=0, end_colx=10)
		# get rid of the root line
		if rowValues[0].encode('utf-8') == 'root': continue
		# get rid of the unnecessary heading line 
		if rowValues[2].encode('utf-8') == 'b     ċ      d': continue
		# if there are variants, find them and append them to the right key
		for x in range(len(rowValues)):
			if rowValues[0].encode('utf-8') == '':
				if rowValues[x].encode('utf-8') != '': 
					try: 
						# If there's already two, add it to a list. Or, make a list.
						try: 
							assert isinstance(verbs[lastRowValues.encode('utf-8')][x-1], basestring)
							if len(rowValues[x]) > 1 and rowValues[x][-1] == ',': rowValues[x] = rowValues[x][:-1]
							verbs[lastRowValues.encode('utf-8')][x-1] = [verbs[lastRowValues.encode('utf-8')][x-1], rowValues[x].encode('utf-8')]
						except:
							assert not isinstance(verbs[lastRowValues.encode('utf-8')][x-1], basestring)
							if len(rowValues[x]) > 1 and rowValues[x][-1] == ',': rowValues[x] = rowValues[x][:-1]
							verbs[lastRowValues.encode('utf-8')][x-1].append(rowValues[x].encode('utf-8'))
					except: pass
				else: pass
			else: pass
		# Strip the errant commas
		else: 
			variations = []
			for variant in rowValues[1:]:
				if len(variant) > 1 and variant[-1] == ',': variant = variant[:-1]
				variations.append(variant.encode('utf-8').strip())
			verbs[rowValues[0].encode('utf-8')] = variations
		# If this is on a new line and there is a variant that needs to be added to the last item
		if rowValues[0].encode('utf-8') != '':
			lastRowValues = rowValues[0]
		# Testing code to see it as it updates.
		#if lastRowValues:
			#print lastRowValues, verbs[lastRowValues.encode('utf-8')]
	# And close the output file. 
	return verbs
	
def printout(storage):
	f = open(output_file, 'w+') #Open up the output file for writing. 
	#
	# Figure out how to print this damn thing later
	#
	for keys in storage:
		string = str(keys) + ',' + storage[keys]
	print(string)
	f.write(string)
	f.close()

if __name__ == "__main__":
	if sys.argv[1] == 'grab': grab()
	if sys.argv[1] == 'print': printout(grab())