import sys, os
import shutil
import getopt
import datetime
import pprint
import stat
import platform

__version__ = '1.1 2021-04-27'
__author__  = '(c) 2019,2021 Frans Schippers (f.h.schippers@hva.nl) for SMP/Python'

import opg2a

gRefInfos = [
    # Subdirectories below Parent-directory, Order is important
    { 'dname': '',         'fname': '',      'typ': 'd', 'mode': 'rwxr-xr-x', 'size': -1,                      },
    { 'dname': '',         'fname': 'dir',   'typ': 'd', 'mode': 'rwxr-xr-x', 'size': -1,                      },
    { 'dname': '',         'fname': 'file1', 'typ': 'f', 'mode': 'rw-r--r--', 'size':  7, 'data': b'text1\r\n' },
    { 'dname': '',         'fname': 'file2', 'typ': 'f', 'mode': 'rw-r--r--', 'size':  7, 'data': b'text2\r\n' },
    { 'dname': 'dir' ,     'fname': 'dir3',  'typ': 'd', 'mode': 'rwxr-xr-x', 'size': -1,                      },
    { 'dname': 'dir/dir3', 'fname': 'file3', 'typ': 'f', 'mode': 'rwxr--r--', 'size':  7, 'data': b'text3\r\n' },
]
# Update path for window
if platform.system() == 'Windows':
    for fInfo in gRefInfos:
        fInfo['dname']  = os.path.join(*fInfo['dname'].split('/'))
        if fInfo['typ'] == 'd': fInfo['mode'] = 'rwxrwxrwx'


def un_filemode(mode_str):
    mode = 0
    for char, table in zip(mode_str, stat._filemode_table):
        for bit, bitchar in table:
            if char == bitchar:
                mode |= bit
                break
    return mode

def normPath(path):
    if path.endswith('/') or path.endswith('\\'):
        return path[:-1]
    return path

def setup(dname):
    if os.path.exists(dname):
        shutil.rmtree(dname)

    for fInfo in gRefInfos:
        path = normPath(os.path.join(dname, fInfo['dname'], fInfo['fname']))
        
        if fInfo['typ'] == 'd':
            os.mkdir(path)
        elif fInfo['typ'] == 'f':
            with open(path, 'wb') as fp:
                fp.write(fInfo['data'])
        else:
            print(f"Error: Unknown file-type: path={path}, typ={fInfo['typ']}")

    for fInfo in reversed(gRefInfos):
        # First set mode of subfiles, than parent directory
        path = normPath(os.path.join(dname, fInfo['dname'], fInfo['fname']))
        mode = un_filemode('-'+fInfo['mode'])
        os.chmod(path, mode)

def check(lines, dname):
    stdInfos = []
    for line in lines:
        fInfo = { kv.split(':')[0]: kv.split(':')[1] for kv in line.split(',') }
        stdInfos.append(fInfo)
    refDct = { normPath(os.path.join(dname, fInfo['dname'], fInfo['fname'])): fInfo \
            for fInfo in gRefInfos }
    stdDct = { normPath(os.path.join(fInfo['dname'], fInfo['fname'])): fInfo for fInfo in stdInfos  }
    refFnames = set(refDct.keys())
    stdFnames = set(stdDct.keys())

    errs = []
    for fname in refFnames.difference(stdFnames):
        errs.append('Error: Missing file: {}'.format(fname))
    for fname in stdFnames.difference(refFnames):
        errs.append('Error: Extra   file: {}'.format(fname))

    for fname in refFnames.intersection(stdFnames):
        if stdDct[fname].get('mode') != refDct[fname].get('mode'):
            if platform.system() == 'Windows':
                errs.append('Warning: {} mode niet getest on Windows'.format(fname))
            else:
                errs.append('Error: {} mode: {} != {}'.format(fname, stdDct[fname].get('mode'), refDct[fname].get('mode')))

        if refDct[fname]['typ'] == 'f' and refDct[fname].get('size'):
            if int(stdDct[fname].get('size')) != refDct[fname].get('size'):
                errs.append('Error: {} size: {} != {}'.format(fname, stdDct[fname].get('size'), refDct[fname].get('size')))

        try:
            dt = datetime.datetime.strptime(stdDct[fname].get('mtime', ''), '%Y%m%d%H%M%S')
        except:
            errs.append('Error: {} mtime: {}: not a timestammp'.format(fname, stdDct[fname].get('mtime')))

        try:
            sz = int(stdDct[fname].get('size', ''))
        except:
            errs.append('Error: {} size: {}: not a size'.format(fname, stdDct[fname].get('size')))
    return errs

if __name__ == '__main__':
    testdir='opg2a_testdir'
    setup(testdir)
    fsInfo = opg2a.scan(testdir, '')
    res = opg2a.show(fsInfo)
    errs = check(res, testdir)
    if errs:
        for err in errs:
            print(err)
        print('Tests failed')
    else:
        print('Tests passed')
    sys.exit(1 if errs else 0)

