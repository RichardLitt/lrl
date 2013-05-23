Maltese.py
-------
The Maltese dictionary script works by looking up Maltese or English
words in an online dictionary. To run, save the file onto your computer. Then, `cd` to the folder where the file is on your computer: for instance, `cd Desktop/`. Then, run these commands:

    python maltese.py e bear
    python maltese.py m ors
    python maltese.py list 10

And you should see the output and be able to go from there. I also
suggest setting up an alias:

    ln -s /path/to/file/maltese.py /usr/bin/maltese

Gooey-Maltese.py
----------------

This script is very similar to the Maltese script at the moment, but
with an integrated GUI coded in wxPython. It needs wxPython to be
installed. I would suggest either getting it manually online or trying:

    easy_install wxpython

This is still in development, but the beta works fine. It has not yet
been packaged for Mac OSX. It should be usable cross-platorm. 
