"""
This script generate the statistics of a web service operation and messages
"""





import xml.etree.ElementTree as etree

class FourDHandler():

	def __init__(self):
		self._tree = etree.parse('4DWSDL.xml')
		self._root = self._tree.getroot()
		self._all_message = self._root.findall('{http://schemas.xmlsoap.org/wsdl/}message')
		self._single_portType = self._root.findall('{http://schemas.xmlsoap.org/wsdl/}portType')
		self._all_binding = self._root.findall('{http://schemas.xmlsoap.org/wsdl/}binding')
		
		
	def countMessage(self):
		for _single_portType in self._single_portType:
			_operations = _single_portType.findall('{http://schemas.xmlsoap.org/wsdl/}operation')
			print 'Operation count in portType: ' + str(len(_operations))
		
		print 'Message count: ' + str(len(self._all_message))
			
	def countOperation(self):
		for _single_portType in self._all_binding:
			_operations = _single_portType.findall('{http://schemas.xmlsoap.org/wsdl/}operation')
			print 'Operation count in Binding: ' + str(len(_operations))

		
	def countAll(self):
		self.countMessage()
		self.countOperation()
	
		
		
	

			
if ( __name__ == "__main__"):
	
	MyHandler = FourDHandler();
	
	#MyHandler.printTableName()
	
	#MyHandler.getTableLength()
	
	MyHandler.countAll()