# This Python script will retrieve a file named 'EOSL.csv' from AWS S3 bucket
#
# Install Python 2.7.10 (64 bit):
#       https://www.python.org/downloads/release/python-2710/
#       https://docs.python.org/3/using/
#
#       C:\> set path=%path%;C:\Python27;C:\Python27\Scripts;C:\Python27\Tools\Scripts
#	
#       C:\> Python   -- starts the interpreter
#
#	C:\> Python <script.py> -- runs script.py
#
#	
# AWS Software Developers Kit (SDK) for Python is called Boto3
#	
#	https://aws.amazon.com/sdk-for-python/
#	https://pypi.python.org/pypi/boto3/#downloads
#
#
#	Boto3 documentation:
#	      https://boto3.readthedocs.io/en/latest/guide/quickstart.html
#
# Install AWS Boto3 onto local machine
#	C:\> pip install boto3
#	
#	Sign into AWS account in web browser: http:\\aws.amazon.com
#
#	Click on IAM Management (to manage identities)
#       Create a new user: "voodoolabs1"
#            This will generate API credentials:
#		Access Key ID: ...........................
#		Secret Access Key: .............................
#
#	Grant S3 full access permissions policy to "voodoolabs1"
#	
#       Using GUI Create a bucket in the S3 service called 'voodoobucket1'
#
#	Using GUI, Upload a sample file to voodoobucket1:  "EOSL.csv"
#
#	Install AWS cli for Windows:    https://aws.amazon.com/cli/
#
#	C:\> aws configure
#	Enter Access Keys generated in the AWS GUI
# 	AWS Access Key ID: <paste it here>
#	AWS Secret Access Key: <paste it here>
#	Default region name: us-east-1
#
#	To run this script:
#
#	C:\> python download_eosl_from_s3.py
	
import boto3
# Let's use Amazon S3
s3 = boto3.resource('s3')


# Now that you have an s3 resource, you can make requests and
# process responses from the service. The following uses the
# buckets collection to print out all bucket names.
	

# It's also easy to upload and download binary data. For
# Example, the following uploads a new file to S3. It assumes
# that the bucket voodoolabs already exists. And it assumes
# the file "test.txt" exists in the local directory
# 
# Upload a new file:
#   data = open('test.txt', 'rb')
#   s3.Bucket('voodoolabs').put_object(Key='test.txt', Body=data)
#   Log into AWS account and verify that 'text.txt' is now in the S3 Bucket voodoolabs


# Read a files from available s3 buckets
for bucket in s3.buckets.all():
    print(bucket.name)
	    
    # output is 'voodoobucket1'

    # Iterates through all the objects, doing the pagination for
    # you. Each obj is an ObjectSummary, so it doesn't contain the
    # body. You'll need to call get to get the whole body.

    for obj in bucket.objects.all():
    	key = obj.key
	print key
    	body = obj.get()['Body'].read()
	print body
	
        # Output is:
	# EOSL.csv
	# cat of EOSL.csv

