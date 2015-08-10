"""
This script update project menu timestamp after a scheduled Jenkin build
"""

from bs4 import BeautifulSoup
import datetime
import sys
import re

def processCode(projectName):

	CayentaWebMenu = 'D:\Servers\Tomcat7\webapps\ROOT\menu.html'

	f = open(CayentaWebMenu, 'r')

	soup = BeautifulSoup(f.read(),  from_encoding="UTF-8")

	for link in soup.find_all('a'):
		result = re.findall('\\b'+projectName+'\\b', link.string)
		if len(result) > 0 and 'core' not in projectName.lower():
			link.string = projectName + ' (' + datetime.datetime.now().isoformat() + ')'	
		if len(result) > 0 and 'core' in projectName.lower():
			link.string = projectName + '(some defect, will fix. timestamp:' + datetime.datetime.now().isoformat() + ')'
			
	prettyHTML =  soup.prettify()
	
	f = open(CayentaWebMenu, 'w')
	f.write(prettyHTML)
	f.close()
	
def main():
	try:
		projectName =  sys.argv[1]
		processCode(projectName)
	except IndexError:
		print 'Please provide a project name'
		
if __name__ == "__main__":
	main()