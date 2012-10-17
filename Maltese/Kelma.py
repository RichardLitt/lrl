### Notes:
### You're trying to install the new dictionary
### To switch back. 
### Turn internet to True
### Rename old dictionary back
### open file without using URLlib
### edit the bottom __main__

#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
#####################################################################
# This uses an online dictionary of Maltese - English and makes a little
# terminal-side random flashcard and lookup tool. As the dictionary is
# copyrighted, one can either download it locally or just use the script here
# as is to access the website if you have internet. The script will check if
# you have internet or not.
#
# WTFPL copyright. Released into the wild by Richard Littauer. 
#####################################################################

import sys
import wx
import random
import re
import urllib2
from BeautifulSoup import BeautifulStoneSoup
import string

############################################################
# Test if the internet is on or not using Google.
# From: http://stackoverflow.com/questions/3764291/checking-network-connection
############################################################
'''
# Not needed anymore given the new dictionary
def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.113.99',timeout=1)
        ##### Change back to True if you want to use the internet again
        return False
    except urllib2.URLError as err: pass
    return False

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
                #file = open('Basic Dictionary.xml', 'r+')
                file = urllib2.urlopen('Basic Dictionary.xml')
                local = True
            except: 
                print ' I couldn\'t find the dictionary. \
                Ma stajtx insib din id-dizzjunarju.'
            status = 'off'
'''

# Stops this damn 'None' from appearing. Couldn't track it down.
# http://stackoverflow.com/a/1034598/1166929
def xtr(s): return '' if s is None else str(s)

'''
# Just sorts the dictionary roughly, cleaning out the extra html.
def sort():
    dict = []
    for line in file:
        line = line.strip().split('   ')
        if len(line) == 3:
            dict.append(line)
    return dict
'''

def iterator():
    file = open('Basic Dictionary.xml', 'r+')
    bs = BeautifulStoneSoup(file)
    entries = bs.findAll('entry')
    return entries

iterator = iterator()

def souper(language, word, depth):
    out = []
    reword = re.compile(word, re.IGNORECASE)
    if language == 'm': 
        for entry in iterator:
            kelma = entry.findAll('quote')
            for kelm in kelma:
                if depth == 'l':
                    match = re.search(reword, kelm.contents[0])
                    if match != None:
                        out += [entry]
                if depth == 'm':
                    match = re.match(reword, kelm.contents[0])
                    if match != None:
                        out += [entry]
                if depth == 'e':
                    if word == kelm.contents[0]:
                        out += [entry]
    if language == 'e':
        for entry in iterator:
            kelma = entry.find('orth')
            if depth == 'l':
                match = re.search(reword, kelma.contents[0])
                if match != None:
                    out += [entry]
            if depth == 'm':
                match = re.match(reword, kelma.contents[0])
                if match != None:
                    out += [entry]
            if depth == 'e':
                if kelma.contents[0].lower() == word:
                    out += [entry]
    return out

def printer(souper):
    find = False
    if souper != []:
        find = True
        for entry in souper:
            out = ''
            out += entry.find('orth').contents[0].swapcase() + '......'
            if entry.find('gen') != None:
                out += entry.find('pos').contents[0].swapcase() + ' ('
                out += entry.find('gen').contents[0].swapcase() + ')......'
            else: 
                try: out += entry.find('pos').contents[0].swapcase() + '......'
                except: out += '...'
            s = []
            p = ''
            senses = entry.findAll('sense')
            if len(senses) != 1:
                s = ''
                for sense in senses:
                    s += sense.find('quote').contents[0] \
                    + ' [' + sense.find('pron').contents[0] + '], '
                out += s.strip(', ')
            if len(senses) == 1:
                out += senses[0].find('quote').contents[0] \
                + ' [' + senses[0].find('pron').contents[0] + ']'
            print out
    if find == False:
        print " I couldn't find this word. Ma stajtx insib din il-kelma."

'''
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
'''

##################################################
# From: redirectText.py, Created by Mike Driscoll#
# Contact: mike@pythonlibrary.org                #
# Website: http://www.blog.pythonlibrary.org     #
##################################################
class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Maltese-English Dictionary",
                size=(600,400))
 
        self.CreateStatusBar() # A StatusBar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        text = wx.StaticText(panel, -1, 'Enter word here:')
        log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,100),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        btn = wx.Button(panel, wx.ID_ANY, 'Search')
        self.word = wx.TextCtrl(panel, wx.ID_ANY, value='', pos=(40, 40), size=(140,20))
        self.Bind(wx.EVT_BUTTON, self.onButton, btn)

        #Maltese or English
        self.rb1 = wx.RadioButton(panel, -1, 'Maltese', style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(panel, -1, 'English ')
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb1.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb2.GetId())
        #self.SetVal(True)

        #Search depth
        self.rbd1 = wx.RadioButton(panel, -1, 'Exact ', style=wx.RB_GROUP)
        self.rbd2 = wx.RadioButton(panel, -1, 'Start ')
        self.rbd3 = wx.RadioButton(panel, -1, 'Entire')
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rbd1.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rbd2.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rbd3.GetId())

        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.LEFT|wx.TOP, 5)
        sizer.Add(self.word, 0, wx.ALL, 5)
        sizer.Add(log, 1, wx.ALL|wx.EXPAND, 10)
        sizer.Add(self.rbd1, 0, wx.LEFT, 5)
        sizer.Add(self.rbd2, 0, wx.LEFT, 5)
        sizer.Add(self.rbd3, 0, wx.LEFT, 5)
        sizer.Add(self.rb1, 0, wx.CENTER)
        sizer.Add(self.rb2, 0, wx.CENTER)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 10)
        #sizer.Add(clearButton, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)

        # redirect text here
        redir=RedirectText(log)
        sys.stdout=redir

        #self.Show()

    # On the search function
    def onButton(self, event):
        if self.rbd1.GetValue() == True:
            if self.rb1.GetValue() == True: 
                print xtr(printer(souper('m', self.word.GetValue(), 'e')))
            else:
                print xtr(printer(souper('e', self.word.GetValue(), 'e')))
        if self.rbd2.GetValue() == True:
            if self.rb1.GetValue() == True: 
                print xtr(printer(souper('m', self.word.GetValue(), 'm')))
            else:
                print xtr(printer(souper('e', self.word.GetValue(), 'm')))
        if self.rbd3.GetValue() == True:
            if self.rb1.GetValue() == True: 
                print xtr(printer(souper('m', self.word.GetValue(), 'l')))
            else:
                print xtr(printer(souper('e', self.word.GetValue(), 'l')))

    #def onClear(self, event):
    #    self.Clear(log)

    def SetVal(self, event):
        state1 = str(self.rb1.GetValue())
        state2 = str(self.rb2.GetValue())

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, \
        '\t Created by Richard Littauer.\n \
        All actual information by someone else.\n \
        Lincensed with a WTFPL License.\n \
        https://github.com/RichardLitt/lrl', \
            "Maltese-English Dictionary", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()
