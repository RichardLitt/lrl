import xlrd # Import the package
book = xlrd.open_workbook(&amp;amp;quot;sample.xls&amp;amp;quot;) # Open an .xls file
sheet = book.sheet_by_index(0) # Get the first sheet
for counter in range(5): # Loop for five times
# grab the current row
rowValues = sheet.row_values(counter,start_col=0, end_colx=4)
# Print the values of the row formatted to 10 characters wide
print &amp;amp;quot;%-10s | %-10s | %-10s | %-10s | %-10s&amp;amp;quot; % tuple(rowValues)
# Print row separator
print &amp;amp;quot;-&amp;amp;quot; *62