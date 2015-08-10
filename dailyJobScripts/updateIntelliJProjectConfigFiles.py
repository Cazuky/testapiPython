"""
This script update some Project set-up property from Flash Builder to IntelliJ
"""

#!/usr/bin/python

import sys, os
import re
import fileinput
import shutil

FILES = False

def main():
    if len(sys.argv) > 2 and sys.argv[2].upper() == '/F':
        global FILES; FILES = True
    try:
        gogogo(sys.argv[1])
    except:
        print('Usage: {} <directory>'.format(os.path.basename(sys.argv[0])))

def tree(path):
    path = os.path.abspath(path)
    dirs, files = listdir(path)[:2]
    print(path)
    walk(path, dirs, files)
    if not dirs:
        print('No subfolders exist')

def walk(root, dirs, files, prefix=''):
    if FILES and files:
        file_prefix = prefix + ('|' if dirs else ' ') + '   '
        for name in files:
            print(file_prefix + name)
        print(file_prefix)
    dir_prefix, walk_prefix = prefix + '+---', prefix + '|   '
    for pos, neg, name in enumerate2(dirs):
        if neg == -1:
            dir_prefix, walk_prefix = prefix + '\\---', prefix + '    '
        print(dir_prefix + name)
        path = os.path.join(root, name)
        try:
            dirs, files = listdir(path)[:2]
        except:
            pass
        else:
            walk(path, dirs, files, walk_prefix)
			
def listdir(path):
    dirs, files, links = [], [], []
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            dirs.append(name)
        elif os.path.isfile(path_name):
            files.append(name)
        elif os.path.islink(path_name):
            links.append(name)
    return dirs, files, links

def enumerate2(sequence):
    length = len(sequence)
    for count, value in enumerate(sequence):
        yield count, count - length, value
		
def findAndReplace(path):	
	for line in fileinput.input(files=[path], inplace=1, backup=".bak"):
		line = re.sub('xyz', 'blahblah', line.rstrip())
		print(line)

		
def findAndPrint(path):	
	with open(path) as f:
		for line in f:
			if "blah" in line:
				print(line)
				
def gogogo(path):
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			if name.endswith('.iml'):
				findAndPrint(os.path.join(root, name))

def revert(path):
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			if name.endswith('.iml'):		
				oldName = os.path.join(root, name)
				srcname = os.path.join(root, name+'.bak')
				shutil.copy2(srcname, oldName)
				#findAndPrint(os.path.join(root, name))
	

if __name__ == '__main__':
    main()
