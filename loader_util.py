import esdclasses
import csv
import boto3


s3bucket = 'voodoobucket1'
hw_filekey = 'EOSL-HW-docu47424.csv'
hw_targetfile = '/tmp/' + hw_filekey


# Read/load data from current directory. 
def load_data():
    result = read_data_into_csv_object(hw_filekey)
    return result
    

# filename is the explicit name (for current dir) of the file, incluing path
# if necessary. For example, it could be "somedata.csv" or "/tmp/somedata.csv".
def read_data_into_csv_object(filename):

    with open (filename, mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
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



# Read the csv data from an S3 bucket. Store to local file system for access.
# Load from local file system.
def load_data_from_s3():
    # First, get a session using the voodoolabs1 user credentials
    # Note: These voodoolabs1 credentials MUST be configured as a profile
    #       in ~/.aws/credentials
    voodoolabsS3 = boto3.Session(profile_name='voodoolabs1')
    
    # Let's use Amazon S3
    s3 = voodoolabsS3.resource('s3')

    # Download object at bucket-name with key-name to tmp.txt
    s3.Bucket(s3bucket).download_file(hw_filekey, hw_targetfile)

    result = read_data_into_csv_object(hw_targetfile)
    return result
