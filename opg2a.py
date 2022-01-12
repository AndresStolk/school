#!/usr/bin/env python3

import sys, os
import getopt
import stat
import datetime

__version__ = '1.0'
__author__  = '(c) 2019,2020 Frans Schippers (f.h.schippers@hva.nl) for SMP/Python'
__opgave__ = 'opg2a.py'

# This is a skeleton implementation.
# You have to replace 'raise NotImplementedError' with your code.
# Update __author__ with your name and studentnr.

def scan(fname, dname):
    """ De eigen schappen van de file worden opgehaald.
        Als het een directory is worden het programma recursief aangeroepen.
        Het is resultaat is een structuur met informatie over de file(s) bv een "list of dicts"
        Zorg dat de uiteindelijke return waarde van deze methode de informatie van alle files bevat.
    """
    fInfos = []
# Student work {{
    dname = 'opg2a_testdir'
    for fname in os.listdir(dname):
        print(fname, os.path.join(dname, fname))
        print(stat.filemode(os.stat(dname).st_mode))

# Student work }}
    return fInfos

print(scan("", ""))

def show(fsInfo):
    """ Show toon te informatie van de verschillende files.
        Voor elke file wordt een beschrijven string gemaakt in de vorm van:
        fname:dir,dname:,mode:rwxr-xr-x,mtime:20200420113520,ino:8662408162,uid:501,uid:0,size:160
        Hierbij fnane, dname, mode, ... de tags en dir, , rwxr-xr-x, 20200420113520 de waarden.
        De retur waarde is een lijst van deze strings die de eigeschappen van de file beschrijven.
        Een lijst wordt teruggegeven en er wordt niet in de methode geprint.
        Dit om automatisch toesen mogelijk te maken
    """
    res = []
    for fInfo in fsInfo:
        pass # remove when "Student work" is filled
# Student work {{
# Student work }}
    return res


if __name__ == '__main__':
    # Handle the options and args
    opts, args = getopt.getopt(sys.argv[1:], '?h')
    for opt, arg in opts:
        if opt in [ '-?', '-h' ]:
            print('Usage: {} -[?h] <file> ...'.format(sys.argv[0],))
            sys.exit()

    # Scan and show the file-system trees
    for dname in args:
        fsInfo = scan(dname, '')
        infos = show(fsInfo)
        for info in infos:
            print(info)
