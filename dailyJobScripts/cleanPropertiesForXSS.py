"""
This script search for unused messages and properties in multiple projects.
"""


import sys
import re

import os, os.path

moduleAPath = "C:\\prj\\xyz771\\core\\src\\main"
moduleBPath = "C:\\prj\\xyz771\\xyz\\src\\main"

	
def exactMatch(line, term):
	searchPhrase = r'\b'+re.escape(term)+r'\b'
	p = re.compile(searchPhrase, re.IGNORECASE)
	
	return bool(p.search(line))

def doesThisFileContainsString(fileName, searchTerm):
	linenum = 1;
	lines = open( fileName, "r" ).readlines()
	for line in lines:
		if exactMatch(line, searchTerm):
			return True, linenum;
		linenum = linenum + 1
	return False, -1;


def walkIt(path, searchTerm):
	ext = ('.java', '.jsp', '.jspf', '.tag')
	for dirpath, dirs, files in os.walk(path):
		for filename in files:
			if filename.endswith(ext):
				fullPath = os.path.join(dirpath, filename)
				ret, linenum = doesThisFileContainsString(fullPath, searchTerm)
				if ret:
					return True, fullPath, linenum
				
	return False, '', -1

def readAppProp(propname, appPath):

	lines = open( appPath, "r" ).readlines()
	fwrite = open(propname +'Result.properties', 'w')
	fwriteNoFound = open(propname + 'NoFound.txt', 'w')
	
	
	for line in lines:
		if '=' in line and not line.startswith('#'):
			key = line.split('=')[0]
			value = line.split('=')[1]
			
			if handleSpecialCaseA(key):
				print 'SPECIAL! Key: ' + key + ' is a special case' +'\n'
					
				fwrite.write(key + '=' + value)
			else:
				found, foundPath, lineNumber = continueWalk(key)
				if found:
					print 'Key: ' + key + ' found Path: ' + foundPath + ' Line Number: ' + str(lineNumber) + '\n'
					
					fwrite.write(key + '=' + value)

				else:
					info = 'NOT FOUND! ' + key +'=' + value + '\n'
					print info
					fwriteNoFound.write(info)
		else:
			fwrite.write(line)
			
	
	fwrite.close();
	fwriteNoFound.close();
	
def continueWalk(key):
	coreFound, coreFoundPath, coreLineNum = walkIt(moduleAPath, key)
	if coreFound:
		return coreFound, coreFoundPath, coreLineNum
	else:
		return walkIt(moduleBPath, key)
	
def handleSpecialCaseA(propName):
	specialCase = ['issueTP', 'menuLink.utilityMainPage.linkLabel', 'menuLinkDescription.utilityMainPage.linkDescription', 'submenu.myOnlineAccount', 'submenu.paymentOptions', 'submenu.utilityRequests',
					'validationForm.accountRegistration.label', 'menuLink.paymentMainPage.linkLabel', 'menuLinkDescription.paymentMainPage.linkDescription','accountValidation.error.message', 'accountValidation.empty.error.message',
					'alert.description','consumption.graph.label', '_PhoneLabel']
	
	for item in specialCase:
		if item in propName:
			return True
		
		
	return False


	
				
if __name__ == "__main__":
	readAppProp('xyzMessages', 'C:\\prj\\xyz771\\Gastonia\\src\\main\\resources\\messages\\messages.properties')
	readAppProp('xyzAppProp', 'C:\\prj\\xyz771\\Gastonia\\src\\main\\resources\\spring\\application.properties')