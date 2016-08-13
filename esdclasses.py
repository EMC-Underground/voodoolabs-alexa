# EMC Support Date Classes

import datetime

tabstr = "	"

# EMCSupportDates is a list of all the DataPoints. 
#	(Each DataPoint is a row of the support dates file)
class EMCSupportDates:
	data = [] 
	lastupdate = ""

	def __init__(self):
		self.data = []
	
	def getlastupdate(self):
		return self.lastupdate.isoformat()
	
	def setlastupdate(self, updatetime):
		self.lastupdate = updatetime
	
	def setlastupdatetonow(self):
		self.lastupdate = datetime.date.today()
	
	def getlen(self):
		return len(self.data)
	
	def getlenstring(self):
		return '{:d}'.format(self.getlen())
		
	# Put a DataPoint on the list. dp is DataPoint
	def push(self, dp):
		self.data.append(dp)
	
	# Get the DataPoint at index from the list. Index starts at 1
	def get(self, index):
		index -= 1
		if index < 0 or index > self.getlen():
			return DataPoint()
		else:
			return self.data[index]
	
	def toJSON(self, indent_level):
	
		tabstring1 = ""
		tabstring2 = ""
		tabstring3 = ""
		jsonstring = ""
		tabs=indent_level
		while tabs > 0:
			tabstring1 = tabstring1 + tabstr
			tabstring2 = tabstring2 + tabstr
			tabstring3 = tabstring3 + tabstr
			tabs -= 1
		tabstring2 = tabstring2 + tabstr
		tabstring3 = tabstring3 + tabstr + tabstr
		
		jsonstring = jsonstring + tabstring1 + '{\n'
		jsonstring = jsonstring + tabstring2 + '"emcsupportdates":\n '
		jsonstring = jsonstring + tabstring2 + '{\n '
		jsonstring = jsonstring + tabstring3 + '"lastupdate": "' + self.getlastupdate() + '",\n'
		jsonstring = jsonstring + tabstring3 + '"numitems": "' + self.getlenstring() + '",\n'
		jsonstring = jsonstring + tabstring3 + '"items":\n'
		jsonstring = jsonstring + tabstring3 + '[\n'
		
		datalen = self.getlen()
		i = 0
		# iterate over the list if items and add each to the string
		for x in self.data:
			i += 1
			jsonstring = jsonstring + x.toJSON(tabs + 4)
			if i < datalen:
				# we're not processing the last element, so add a comma
				jsonstring = jsonstring + ',\n'
			else:
				jsonstring = jsonstring + '\n'
								
		jsonstring = jsonstring + tabstring3 + ']\n'
		jsonstring = jsonstring + tabstring2 + '}\n'
		jsonstring = jsonstring + tabstring1 + "}"
		return jsonstring
	
	
	
	
	
	
# DataPoint is a row of the support dates file
class DataPoint:
	product = ""
	model = ""
	ga_date = ""
	eol_date = ""
	eops_date = ""
	eosl_date = ""
	ga_updated = ""
	eol_updated = ""
	eops_updated = ""
	eosl_updated = ""
	
	dictref = dict()
	
	# Instantiate by passing a dictionary object representing a row of data
	def __init__(self, dictreference):
		
		self.dictref = dictreference
		self.product = dictreference['Product']
		self.model = dictreference['Model']
		self.ga_date = dictreference['GA Date']
		self.eol_date = dictreference['EOL Date']
		self.eops_date = dictreference['EOPS Date']
		self.eosl_date = dictreference['EOSL Date']
		self.ga_updated = dictreference['GA Updated?']
		self.eol_updated = dictreference['EOL Updated?']
		self.eops_updated = dictreference['EOPS Updated?']
		self.eosl_updated = dictreference['EOSL Updated?']
		
		
	def getproduct(self):
		return self.product
	
	def getmodel(self):
		return self.model
	
	def getgadate(self):
		return self.ga_date
		
	def geteoldate(self):
		return self.eol_date
		
	def geteopsdate(self):
		return self.eops_date
		
	def geteosldate(self):
		return self.eosl_date
	
	def getgaupdated(self):
		return self.ga_updated
		
	def geteolupdated(self):
		return self.eol_updated
		
	def geteopsupdated(self):
		return self.eops_updated
		
	def geteoslupdated(self):
		return self.eosl_updated
		
	def getfieldnames():
		return ['Product', 'Model', 'GA Date', 'EOL Date', 'EOPS Date', 
					'EOSL Date', 'GA Updated?', 'EOL Updated?', 
					'EOPS Updated?', 'EOSL Updated?']
	
	def toJSON(self, indent_level):
	
		tabstring1 = ""
		tabstring2 = ""
		jsonstring = ""
		tabs=indent_level
		while tabs > 0:
			tabstring1 = tabstring1 + tabstr
			tabstring2 = tabstring2 + tabstr
			tabs -= 1
		tabstring2 = tabstring2 + tabstr
		
		jsonstring = jsonstring + tabstring1 + "{\n"
		jsonstring = jsonstring + tabstring2 + '"product": "' + self.getproduct() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"model": "' + self.getmodel() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"gadate": "' + self.getgadate() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"eoldate": "' + self.geteoldate() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"eopsdate": "' + self.geteopsdate() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"eosldate": "' + self.geteosldate() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"gaupdated": "' + self.getgaupdated() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"eolupdated": "' + self.geteolupdated() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"eopsupdated": "' + self.geteopsupdated() + '",\n'
		jsonstring = jsonstring + tabstring2 + '"eoslupdated": "' + self.geteoslupdated() + '",\n'
		jsonstring = jsonstring + tabstring1 + "}"
		return jsonstring
		
	#def toJSON(self):
	#	self.toJSON(0)
	
