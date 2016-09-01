import esdclasses
import csv


def load_data():

    with open ('EOSL.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
	reader = csv.DictReader(csvfile, dialect='excel')
	
	alldata = esdclasses.EMCSupportDates()
	alldata.setlastupdatetonow()
	
        i=0
        
        #begin supportdates
        for row in reader:
                i += 1
                
                # skip the first one because it will be the header row
                if i > 1:
                        thisone = esdclasses.DataPoint(row)
                        alldata.push(thisone)
        

        #end supportdates

    	csvfile.close()

        return alldata
