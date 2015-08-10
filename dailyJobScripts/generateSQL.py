"""
This script convert a legacy database table structure from XML format to MySQL file
"""

import xml.etree.ElementTree as etree

class TableStructureHandler():

	def __init__(self):
		self._root = etree.parse('iClinicDB.xml').getroot()
		self._all_table = self._root.findall('table')
		
		
	def printTableName(self):
		for _single_table in self._all_table:
			print _single_table.attrib['name']
			
	def getTableLength(self):
		print 'Table count: ' + str(len(self._all_table))
		return len(self._all_table)
		
	def printFirstTableFieldName(self):
		_cur_table = self._all_table[1]
		for _single_field in _cur_table.findall('field'):
			print 'Table name: ' + _cur_table.attrib['name'] + '; Field name: ' + _single_field.attrib['name']
			
	def checkNull(self, key, field):
		if key in field.attrib:
			return field.attrib[key]
		return 'N/A'
		
	def printSpecificTableInfo(self, inx):
		_cur_table = self._all_table[inx]
		for _single_field in _cur_table.findall('field'):
			print 'Table name: ' + _cur_table.attrib['name'] + '; Field name: ' + _single_field.attrib['name'] + '; Type: ' + _single_field.attrib['type'] + \
			'; Never Null: '+ self.checkNull('never_null', _single_field) + '; Limiting Length: ' + self.checkNull('limiting_length',_single_field)
	
	
	def fieldChecker(self, inx):
		_cur_table = self._all_table[inx]
		for _single_field in _cur_table.findall('field'):
			if _single_field.attrib['type'] == '10':
				print 'Table name: ' + _cur_table.attrib['name'] + '; Field name: ' + _single_field.attrib['name'] + '; Type: ' + _single_field.attrib['type'] + \
				'; Never Null: '+ self.checkNull('never_null', _single_field) + '; Limiting Length: ' + self.checkNull('limiting_length',_single_field)
				
	def getAllTypes(self):
		_type_list = []
		for inx in range(len(self._all_table)):
			_cur_table = self._all_table[inx]
			for _single_field in _cur_table.findall('field'):
				print _single_field.attrib['name']
				if _single_field.attrib['type'] not in _type_list:
					_type_list.append(_single_field.attrib['type'])		
		print ",".join(_type_list)
		
	def generateFieldSQL(self, _all_fields):
		line = []
		_unique_columns = []
		for _single_field in _all_fields:
			if _single_field.attrib['name'] != 'filler' and _single_field.attrib['name'] not in _unique_columns:
				_unique_columns.append(_single_field.attrib['name'])
				line.append(self.generateSingleFieldSQL(_single_field))
		
		return ',\n'.join(line)
		
	def generateSingleFieldSQL(self, field):
		_field_type = field.attrib['type']
		_field_name = field.attrib['name']
		_field_null = self.checkNull('Never Null', field)
		_field_length = self.checkNull('limiting_length', field)
		
		line = "\t`"+_field_name+"`\t"
		
		
		#Boolean type
		if _field_type == '1':
			line = line + 'BOOLEAN'
	
		#Integer
		if _field_type == '3':
			line = line + 'INTEGER'
			
		#Long Integer
		if _field_type == '4':
			line = line + 'BIGINT'
			
		#REAL
		if _field_type == '6':
			line = line + 'REAL'
		
		#DATE YYYYMMDD
		if _field_type == '8':
			line = line + 'DATE'
			
		#Time hh:mm:ss
		if _field_type == '9':
			line = line + 'TIME'
			
		#Text with size
		if _field_type == '10':
			
			if _field_length == 'N/A':
				line = line + 'TEXT'
			else:
				line = line + 'VARCHAR('+_field_length+')'
		#General Text
		if _field_type == '14':
			line = line + 'TEXT'
		
		#Blob
		if _field_type == '18':
			line = line + 'BLOB'
		
		
		return line
		

	def generateAllScriptsMultiple(self):
		for inx in range(len(self._all_table)):
			self.genereateSingleTableScript(inx)
			
			
	def printSQLScript(self):
		_cur_table = self._all_table[0]
		_all_fields = self._all_table[0].findall('field')
		self.generateSQLScript(_cur_table, _all_fields)

			
			
	def generateSQLScript(self, table_name, _all_fields):
		line = "DROP TABLE IF EXISTS `"+table_name.attrib['name']+"`;\n" + \
		"CREATE TABLE `"+table_name.attrib['name']+"` (\n"+ \
		self.generateFieldSQL(_all_fields)+"\n" + \
		")"
		
		return line
	
	def genereateSingleTableScript(self, inx):
		_cur_table = self._all_table[inx]
		_all_fields = _cur_table.findall('field')
		line = self.generateSQLScript(_cur_table, _all_fields)
		self.writeToFileMultiple(line, _cur_table.attrib['name'])


		
	def writeToFileMultiple(self, line, table_name):
		file_path = 'generatedSQLScripts\\multiple\\'+table_name+'.sql'		
		sql_file = open(file_path, "w+")		
		sql_file.write(line)
		sql_file.close()
	
	def writeToSingleBigFile(self, line):
		file_path = 'generatedSQLScripts\\iclinicDB.sql'		
		sql_file = open(file_path, "w+")		
		sql_file.write(line)
		sql_file.close()
	
	def generateAllScriptSingleFile(self):
		line = ''
		for inx in range(len(self._all_table)):
			_cur_table = self._all_table[inx]
			_all_fields = _cur_table.findall('field')
			if len(_all_fields) != 0:
				line = line + self.generateSQLScript(_cur_table, _all_fields) + ';\n'
			
		self.writeToSingleBigFile(line)
			
			
	
		
		
	

			
if ( __name__ == "__main__"):
	
	MyHandler = TableStructureHandler();
	
	#MyHandler.printTableName()
	
	#MyHandler.getTableLength()
	
	MyHandler.generateAllScriptSingleFile()