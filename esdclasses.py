# EMC Support Date Classes

import datetime

tabstr = "	"

# EMCSupportDates is a list of all the DataPoints. 
#	(Each DataPoint is a row of the support dates file)
class EMCSupportDates:
	data = [] 
	lastupdate = ""
	productslist = []  # list containing all products in data exactly once
	modelslist = [] # list containing all models in data exactly once

	def __init__(self):
		self.data = []
		self.productslist = []
                self.modelslist = []
                
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

	def getproductslist(self):
		return self.productslist
		
        def rebuildproductslist(self):
                self.productslist = []
                for x in self.data:
                        self.add_iff_unique( self.productslist,
                                             x.getproduct().strip() )

	def getmodelslist(self):
		return self.modelslist

        def rebuildmodelslist(self):
                self.modelslist = []
                for x in self.data:
                        self.add_iff_unique( self.modelslist,
                                             x.getmodel().strip() )
                        

        # if someitem is not already in somelist, append it.
        # somelist must be of python list type
        # ensure that someitem is of the type you'll be expecting when you
        # access the list
        def add_iff_unique(self, somelist, someitem):
               if someitem not in somelist:
                        # add only when not already in the list
                        somelist.append( someitem )

	# Put a DataPoint on the list. dp is DataPoint
	def push(self, dp):
		self.data.append(dp)
		self.add_iff_unique( self.productslist, dp.getproduct() )
		self.add_iff_unique( self.modelslist, dp.getmodel() )
	
	# Get the DataPoint at index from the list. Index starts at 1
	def get(self, index):
		index -= 1
		if index < 0 or index > self.getlen():
			return DataPoint()
		else:
			return self.data[index]


	def find_matches_by_product(self, product):
                new_esd = EMCSupportDates()
		# iterate over the list of items and add each to the string
		for x in self.data:
                        supplied = new_esd.clean_string_for_comparison(product)
                        thisdp = new_esd.clean_string_for_comparison(x.getproduct())
                        #print("-----comparing: " + supplied + " == " + thisdp)
			if thisdp == supplied:
				new_esd.push(x.clone())
				#print("------- MATCH")
				#print(x.toSimpleString())
		return new_esd


	def find_matches_by_model(self, model):
                new_esd = EMCSupportDates()
		# iterate over the list of items and add each to the string
		for x in self.data:
                        supplied = new_esd.clean_string_for_comparison(model)
                        thisdp = new_esd.clean_string_for_comparison(x.getmodel())
                        #print("-----comparing: " + supplied + " == " + thisdp)
			if thisdp == supplied:
				new_esd.push(x.clone())
				#print("------- MATCH")
                                #print(x.toSimpleString())
		return new_esd

        # clean up a string so that it can be compared
        def clean_string_for_comparison(self, astring):
                newstring = astring.lower()

                # remove commas (yes, Alexa might insert them)
                newstring = newstring.replace(",", "")

                # remove spaces (often happens when converting from speech)
                newstring = newstring.replace(" ", "")

                # some of the data points have parentheses
                newstring = newstring.replace(")", "")
                newstring = newstring.replace("(", "")

                # some of the data points have dashes
                newstring = newstring.replace("-", "")

                return newstring

	
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
		# iterate over the list of items and add each to the string
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
	
	
	def toSimpleString(self):
	
		simplestring = ""
		simplestring = simplestring + 'There are ' + self.getlenstring() + ' items in this list.\n' 
		
		datalen = self.getlen()
		i = 0
		# iterate over the list of items and add each to the string
		for x in self.data:
			i += 1
			simplestring = simplestring + 'Item number ' + '{:d}'.format(i) + " of " + '{:d}'.format(datalen) + ": "

			simplestring = simplestring + x.toSimpleString()
			if i < datalen:
				# we're not processing the last element, so add a comma
				simplestring = simplestring + '\n '
			else:
				simplestring = simplestring + '.'
								
		#simplestring + '"File last queried on": "' + self.getlastupdate() + '",\n'
		return simplestring
	
	
	
	
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
		

	def getdictreference(self):
		return self.dictref
		
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

        def fill_string_if_empty(self, astring):
                resultstring = astring
                if astring == "":
                        resultstring = "Not Set"
                return resultstring
                        

	# Instantiate as a copy of another DataPoint object 
	def clone(self):  #dpo is a DataPoint object
		return DataPoint(self.getdictreference())
                
	def toSimpleString(self):
	
		simplestring = ""
		simplestring = simplestring + self.getproduct() + ' ' +  self.getmodel() + ' has the following support dates: '
		simplestring = simplestring + initialsInString('GA') + ' Date: ' + self.fill_string_if_empty(self.getgadate()) + ', '
		simplestring = simplestring + initialsInString('EOL') + ' Date: ' + self.fill_string_if_empty(self.geteoldate()) + ', '
		simplestring = simplestring + initialsInString('EOPS') + ' Date: ' + self.fill_string_if_empty(self.geteopsdate()) + ', '
		simplestring = simplestring + initialsInString('EOSL') + ' Date: ' + self.fill_string_if_empty(self.geteosldate())
		return simplestring

        def initialsInString(self):

                sendstring = "<say-as interpret-as=\"characters\">" + self + "</say-as>"
                return sendstring
		
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
	
