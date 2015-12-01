#This script is created for switching between development and release profile during a jenkin build. It changes spring.profiles.default on web.xml file

import xml.etree.ElementTree as ET


def updateProfile(file_path):
	ET.register_namespace("","http://xmlns.jcp.org/xml/ns/javaee")
	doc = ET.parse(file_path);
	root = doc.getroot();
	xml_link = '{http://xmlns.jcp.org/xml/ns/javaee}'
	for context_param in root.findall(xml_link+'context-param'):
		for child in context_param:
			if child.text == 'spring.profiles.default':
				context_param[1].text = 'release';
				break;
				
	
	f = open('webnew.xml', 'w')
	f.write(ET.tostring(root, encoding="UTF-8", method="xml"))
	f.close()
	
				
def main():
	updateProfile('web.xml');

if __name__ == "__main__":
	main()